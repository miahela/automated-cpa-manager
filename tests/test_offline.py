"""Offline regressions. External imports are omitted; no browser or API starts."""
import ast
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from functions.load_config import load_config

ROOT = Path(__file__).resolve().parents[1]


def local_class(filename, name, **namespace):
    tree = ast.parse((ROOT / filename).read_text())
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == name)
    exec(compile(ast.Module(body=[node], type_ignores=[]), filename, "exec"), namespace)
    return namespace[name]


class OfflineTests(unittest.TestCase):
    def test_config_paths_and_bom(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as directory:
            path = Path(directory) / 'config.json'
            path.write_text(json.dumps({'landing_pages': 'pages'}), encoding='utf-8-sig')
            with patch.dict(os.environ, CPA_CONFIG=str(path)):
                self.assertEqual(load_config()['landing_pages'], str(path.parent / 'pages'))

    def test_browser_action_failure_propagates(self):
        cls = local_class('classes/SeleniumManager.py', 'SeleniumManager',
                          EC=Mock(), By=Mock())
        manager = cls.__new__(cls)
        manager.logger = Mock()
        manager.wait = Mock()
        manager.wait.until.side_effect = RuntimeError('missing button')
        with self.assertRaises(RuntimeError):
            manager.click_element('//missing')
        with self.assertRaises(RuntimeError):
            manager.fill_field('//missing', 'value')
        with self.assertRaises(RuntimeError):
            manager.wait_until_url_changes('old')
        manager.driver = Mock()
        manager.driver.get.side_effect = RuntimeError('navigation failed')
        with self.assertRaises(RuntimeError):
            manager.open_link('https://example.com')

    def test_browser_restores_first_tab_and_passes_script_arguments(self):
        cls = local_class('classes/SeleniumManager.py', 'SeleniumManager')
        manager = cls.__new__(cls)
        manager.logger = Mock()
        manager.driver = Mock()
        manager.driver.window_handles = ['first', 'second']
        manager.close_all_tabs_except_first()
        manager.driver.switch_to.window.assert_called_with('first')
        manager.add_local_storage("a'b", 'value')
        manager.driver.execute_script.assert_called_with(
            'localStorage.setItem(arguments[0], arguments[1]);', "a'b", 'value')
        manager.add_cookies([{'name': 'session', 'value': 'fake', 'domain': '.example.com'}])
        self.assertEqual(manager.driver.add_cookie.call_args.args[0]['domain'], '.example.com')

    def test_content_deletion_uses_xpath_based_routine(self):
        cls = local_class('ContentUpdater.py', 'ContentUpdater')
        manager = cls.__new__(cls)
        manager.web_hosting_manager = Mock()
        manager.delete_old_content()
        manager.web_hosting_manager.delete_old_files.assert_called_once_with()

    def test_cache_retry_independent_of_https(self):
        cls = local_class('HTTPS_CacheCleaner.py', 'HTTPS_CacheCleaner', true='TRUE', false='FALSE')
        manager = cls.__new__(cls)
        manager.google_sheets_manager = Mock()
        manager.google_sheets_manager.get_domains_by_condition.side_effect = [[], ['landing.example']]
        manager.web_hosting_manager = Mock()
        manager.web_hosting_manager.flush_cache.return_value = True
        manager.perform_actions()
        manager.web_hosting_manager.https_enforce.assert_not_called()
        manager.google_sheets_manager.update_domain.assert_called_once_with('landing.example', 'Flush Cache', 'TRUE')

    def test_cache_navigates_to_requested_domain(self):
        cls = local_class('classes/WebHostingManager.py', 'WebHostingManager')
        manager = cls.__new__(cls)
        manager.selenium_manager = Mock()
        manager.logger = Mock()
        manager.websites_url = 'https://example.com/sites'
        manager.xpath_config = dict.fromkeys(['speed_side_menu_xpath', 'caching_side_xpath', 'dynamic_cache_xpath', 'flush_action_xpath'], '//button')
        self.assertTrue(manager.flush_cache('landing.example'))
        manager.selenium_manager.open_link.assert_called_once_with(manager.websites_url)
        self.assertIn('landing.example', manager.selenium_manager.click_element.call_args_list[0].args[0])

    def test_upload_returns_success(self):
        cls = local_class('classes/WebHostingManager.py', 'WebHostingManager', os=os, time=Mock(), By=Mock())
        manager = cls.__new__(cls)
        manager.selenium_manager = Mock()
        manager.driver = Mock()
        manager.driver.find_elements.return_value = [Mock()]
        manager.disk_file_manager = Mock()
        manager.landing_pages = 'samples/landing_pages'
        manager.unzip_inside_website = Mock()
        manager.logger = Mock()
        self.assertTrue(manager.upload_new_file({'Type': 'demo', 'Domain': 'landing.example', 'Full Name': 'Sample'}))


if __name__ == '__main__':
    unittest.main()
