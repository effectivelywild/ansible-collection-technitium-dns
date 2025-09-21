# Changelog

## [0.4.0](https://github.com/effectivelywild/ansible-collection-technitium-dns/compare/v0.3.0...v0.4.0) (2025-09-21)


### Features

* add dns_publish_all_keys module ([#19](https://github.com/effectivelywild/ansible-collection-technitium-dns/issues/19)) ([d023620](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/d0236202b38d891e9b176d98e0dcddb18acbdbcb))
* add dns_resync_zone module ([#23](https://github.com/effectivelywild/ansible-collection-technitium-dns/issues/23)) ([7634891](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7634891abc15fba6eb0ba61542b4fb75ed10ae5d))
* add dns_rollover_dnskey module ([76f9e55](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/76f9e556ea6a8477712c87d25ac5877efca7e598))
* add dns_rollover_dnskey module ([#21](https://github.com/effectivelywild/ansible-collection-technitium-dns/issues/21)) ([76f9e55](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/76f9e556ea6a8477712c87d25ac5877efca7e598))
* Add technitium_dns_create_group module ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))
* Add technitium_dns_create_user module ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))
* Add technitium_dns_delete_group module ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))
* Add technitium_dns_delete_user module ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))
* Add technitium_dns_get_group_details module ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))
* Add technitium_dns_get_user_details module ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))
* Add technitium_dns_list_groups module ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))
* Add technitium_dns_list_users module ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))
* Add technitium_dns_set_group_details module ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))
* Add technitium_dns_set_user_details module ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))
* Adding list/set/get/create modules for users and groups ([#24](https://github.com/effectivelywild/ansible-collection-technitium-dns/issues/24)) ([7f3d185](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/7f3d185241f31dcde5bcc74053a2879e79741a65))


### Bug Fixes

* Update some modules to use POST method ([#20](https://github.com/effectivelywild/ansible-collection-technitium-dns/issues/20)) ([a98ea08](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/a98ea0810c770a3f2dbf1e87e1284c7b9ea908dd))


### Documentation

* Add google-site-verification tag to docs site ([f9d86d7](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/f9d86d7c9024a1cd34fdea1d147a95ebb909c953))

## [0.3.0](https://github.com/effectivelywild/ansible-collection-technitium-dns/compare/v0.2.1...v0.3.0) (2025-09-18)


### Features

* add dns_add_private_key module ([#14](https://github.com/effectivelywild/ansible-collection-technitium-dns/issues/14)) ([eddd089](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/eddd0894ac14841ce1ab937dcb8a834aff227ac5))
* add dns_delete_private_key module ([#15](https://github.com/effectivelywild/ansible-collection-technitium-dns/issues/15)) ([4be39da](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/4be39da5eaddc42f2861114ae875c4ab41c2633b))
* add dns_update_dnskey_ttl module ([#16](https://github.com/effectivelywild/ansible-collection-technitium-dns/issues/16)) ([15aa187](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/15aa1878382e4ad1ceeb6519cbefc7478ae72d9f))
* add dns_update_private_key module and integration test ([cb54c33](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/cb54c331d9775e1fe5ea63c343b62ef113ea7317))


### Bug Fixes

* update no_log in argument spec for key_tag ([24aa0d1](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/24aa0d10cce67a41c63b2c630ed36ebbea74fd0c))


### Documentation

* Remove legacy README files from integration tests. ([3fe2b46](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/3fe2b46b6dc61d302ce83c62a8e43f8dbf687a49))
* Update README [skip ci] ([01d99af](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/01d99af073b181568fdc2aa58fbc3d7d9ea97316))

## [0.2.1](https://github.com/effectivelywild/ansible-collection-technitium-dns/compare/v0.2.0...v0.2.1) (2025-09-07)


### Bug Fixes

* add .release-please-manifest.json after switching type to simple ([ef07047](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/ef0704760398fc3eb9a944d95a3d70ea2dc8ef9e))
* migrate release-please config to v4 format with proper galaxy.yml support ([718812b](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/718812b9389bf67e1bb61b23c7c2394eb0353833))
* simplify release-please extra-files config for galaxy.yml ([3c10be4](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/3c10be43a2bd8a45579b97eaec23072def6dcd5d))
* update .release-please-manifest.json with root path ([8f350f5](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/8f350f5824b877e530e77e5960923c022638376c))
* update galaxy.yml version to 0.2.0 and fix release-please config ([a56f0a5](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/a56f0a5f9df313821d55417b0777beea47f31651))
* update release-please config ([3df63c5](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/3df63c52bd340b05a8637222a2f64215b97d28cc))
* update release-please config and ci.yml to properly update galaxy.yml ([89a5d20](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/89a5d20767c1c48d828b35590d9a2af4be097f67))
* update release-please config and ci.yml to properly update galaxy.yml ([894d686](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/894d6868d0cd64f1e5bb29af6cbdb9898c3fe7ac))
* update release-please config and ci.yml to properly update galaxy.yml ([819c341](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/819c341bd72936103511bb4cb7788fbd3921acc8))
* update release-please config to properly handle galaxy.yml YAML file ([d080681](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/d080681d87234796bfbef7f99f9d9c4f52388fda))

## [0.2.0](https://github.com/effectivelywild/ansible-collection-technitium-dns/compare/v0.1.0...v0.2.0) (2025-09-07)


### Features

* add update_nsec3_parameters module ([#4](https://github.com/effectivelywild/ansible-collection-technitium-dns/issues/4)) ([d5323cc](https://github.com/effectivelywild/ansible-collection-technitium-dns/commit/d5323cc388a6eeccc6507a3ab836832b1a7fa424))
