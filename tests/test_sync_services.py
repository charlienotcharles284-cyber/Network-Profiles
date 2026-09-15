import importlib.util
from pathlib import Path
import unittest
spec = importlib.util.spec_from_file_location('sync', Path(__file__).resolve().parents[1] / 'scripts/sync-services.py')
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

class DomainConversion(unittest.TestCase):
    def test_preserves_exact_and_suffix_semantics(self):
        self.assertEqual(sync.domains(['DOMAIN,login.example.com', 'DOMAIN-SUFFIX,example.com', 'DOMAIN-SUFFIX,example.com']), ['+.example.com', 'login.example.com'])
    def test_rejects_empty_or_unsupported_rules(self):
        for payload in ([], None, ['IP-CIDR,1.2.3.0/24'], ['DOMAIN-KEYWORD,example'], ['DOMAIN,https://example.com'], ['DOMAIN,']):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                sync.domains(payload)
