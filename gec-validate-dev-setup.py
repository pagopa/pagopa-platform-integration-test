#!/usr/bin/env python
"""
Validation script for GEC DEV configuration.
Verifies:
  1. dev.yaml is properly loaded
  2. Services.gec config is accessible
  3. Secret key is resolvable
  4. Environment hooks initialize correctly
"""

import os
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s | %(message)s'
)
LOGGER = logging.getLogger(__name__)

def check_dev_yaml():
    """Verify dev.yaml exists and is populated."""
    dev_yaml_path = "src/integration/gec/dev.yaml"
    
    if not os.path.exists(dev_yaml_path):
        LOGGER.error(f"❌ {dev_yaml_path} not found")
        return False
    
    size = os.path.getsize(dev_yaml_path)
    if size == 0:
        LOGGER.error(f"❌ {dev_yaml_path} is empty")
        return False
    
    LOGGER.info(f"✅ {dev_yaml_path} exists ({size} bytes)")
    return True

def check_secrets_yaml():
    """Verify .secrets.yaml exists and dev section is present."""
    secrets_path = "config/.secrets.yaml"
    
    if not os.path.exists(secrets_path):
        LOGGER.warning(f"⚠️  {secrets_path} not found - create from template")
        return False
    
    with open(secrets_path, 'r') as f:
        content = f.read()
        if 'dev:' not in content:
            LOGGER.warning(f"⚠️  {secrets_path} exists but no 'dev:' section")
            return False
        if '<SUBKEY_FROM_ENV>' in content:
            LOGGER.warning(f"⚠️  {secrets_path} has placeholder values - populate with real secret")
            return False
    
    LOGGER.info(f"✅ {secrets_path} has dev section with key")
    return True

def check_load_configurations():
    """Test that load_configurations works."""
    try:
        from src.conf.configuration import load_configurations
        # Must call from repository root (where config/.secrets.yaml is)
        config = load_configurations('src/integration/gec')
        
        LOGGER.info(f"✅ load_configurations() works")
        
        # Dynaconf does case-insensitive attribute lookup
        gec_config = getattr(config, 'gec', None)
        if gec_config:
            LOGGER.info(f"   ✅ 'gec' config found")
            LOGGER.info(f"   GEC URL: {_config_value(gec_config, 'url', 'N/A')}")
            auth_val = _config_value(gec_config, 'auth', {})
            if auth_val:
                LOGGER.info(f"   GEC Auth: {_config_value(auth_val, 'type', 'N/A')}")
            return True
        else:
            LOGGER.warning(f"⚠️  'gec' attribute not found in config")
            if hasattr(config, 'to_dict'):
                actual_keys = [k for k in config.to_dict().keys() if 'DYNACONF' not in k and not k.startswith('_')]
                LOGGER.info(f"   Available custom keys: {actual_keys}")
            return False
            
    except Exception as e:
        LOGGER.error(f"❌ Error loading configuration: {e}")
        import traceback
        traceback.print_exc()
        return False

def _config_value(node, *keys):
    """Read a value from a node recursively."""
    if node is None:
        return None
    if hasattr(node, "to_dict"):
        node = node.to_dict()
    for key in keys:
        if isinstance(node, dict):
            if key in node:
                return node[key]
            for configured_key, value in node.items():
                if str(configured_key).lower() == key.lower():
                    return value
        if hasattr(node, key):
            return getattr(node, key)
    return None


def check_environment_hooks():
    """Test that environment.py hooks can be imported."""
    try:
        from src.integration.gec.environment import before_all
        LOGGER.info(f"✅ environment.before_all() can be imported")
        return True
    except Exception as e:
        LOGGER.error(f"❌ Error importing environment hooks: {e}")
        return False

def check_step_bindings():
    """Test that step bindings can be imported."""
    try:
        import src.integration.gec.steps.feat_001_common_steps
        LOGGER.info(f"✅ Step bindings can be imported")
        return True
    except Exception as e:
        LOGGER.error(f"❌ Error importing step bindings: {e}")
        return False

def main():
    # Set TARGET_ENV before loading any configurations
    os.environ['TARGET_ENV'] = 'dev'
    
    LOGGER.info("=" * 60)
    LOGGER.info("GEC DEV Configuration Validation")
    LOGGER.info("=" * 60)
    
    checks = [
        ("dev.yaml", check_dev_yaml),
        (".secrets.yaml", check_secrets_yaml),
        ("Configuration loader", check_load_configurations),
        ("Environment hooks", check_environment_hooks),
        ("Step bindings", check_step_bindings),
    ]
    
    results = []
    for name, check_fn in checks:
        LOGGER.info(f"\nChecking {name}...")
        try:
            result = check_fn()
            results.append((name, result))
        except Exception as e:
            LOGGER.error(f"❌ Unexpected error in {name}: {e}")
            results.append((name, False))
    
    LOGGER.info("\n" + "=" * 60)
    LOGGER.info("Summary:")
    LOGGER.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        LOGGER.info(f"{status:8s} | {name}")
    
    LOGGER.info(f"\nResult: {passed}/{total} checks passed")
    
    if passed == total:
        LOGGER.info("\n🎉 All checks passed! Ready to run tests.")
        return 0
    else:
        LOGGER.warning(f"\n⚠️  {total - passed} check(s) failed. Review above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
