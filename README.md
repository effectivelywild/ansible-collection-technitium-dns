# Ansible Collection - technetium.dns

[![CI](https://github.com/effectivelywild/ansible-collection-technitium-dns/actions/workflows/ci.yml/badge.svg)](https://github.com/effectivelywild/ansible-collection-technitium-dns/actions/workflows/ci.yml) [![codecov](https://codecov.io/github/effectivelywild/ansible-collection-technitium-dns/graph/badge.svg?token=UVSWMN1RV1)](https://codecov.io/github/effectivelywild/ansible-collection-technitium-dns)

Ansible collection for Technitium DNS based on the [API](https://github.com/TechnitiumSoftware/DnsServer/blob/master/APIDOCS.md).

Almost all API calls have a module matching the call name. If anything is missing please open an issue.

## Contributing to this collection

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you would like to contribute feel free to open a PR with detailed note on our changes. 

* [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html)
* [Ansible Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible Collection Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)


## Compatibility Matrix

This collection is tested against the latest released of Technitium DNS Server.

This collection is tested against the following Ansible and Python versions:

| Ansible Version | Python 3.10 | Python 3.11 | Python 3.12 | Python 3.13 | Python 3.14 |
|----------------|--------------|--------------|--------------|--------------|--------------|
| 2.17           | ✅           | ✅           | ✅           | ❌           | ❌
| 2.18           | ❌           | ✅           | ✅           | ✅           | ❌
| 2.19           | ❌           | ✅           | ✅           | ✅           | ❌
| devel          | ❌           | ❌           | ❌           | ✅           | ✅

**Note:** This matrix reflects our current CI testing coverage. Other combinations may work but are not regularly tested.

## Included content
See the complete list of collection content in the [Plugin Index](https://effectivelywild.github.io/ansible-collection-technitium-dns/collections/index_module.html).

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install effectivelywild.technitium_dns
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Using this collection

Review module [documentation](https://effectivelywild.github.io/ansible-collection-technitium-dns/collections/effectivelywild/technitium_dns/index.html#plugins-in-effectivelywild-technitium-dns) for usage instructions and examples.

## Release notes

See the [changelog](https://github.com/effectivelywild/ansible-collection-technitium-dns/tree/main/CHANGELOG.rst).

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/main/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [News for Maintainers](https://github.com/ansible-collections/news-for-maintainers)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.