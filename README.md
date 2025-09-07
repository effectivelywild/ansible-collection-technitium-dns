# Ansible Collection - technetium.dns

[![CI](https://github.com/effectivelywild/ansible-collection-technitium-dns/actions/workflows/ci.yml/badge.svg)](https://github.com/effectivelywild/ansible-collection-technitium-dns/actions/workflows/ci.yml) [![codecov](https://codecov.io/github/effectivelywild/ansible-collection-technitium-dns/graph/badge.svg?token=UVSWMN1RV1)](https://codecov.io/github/effectivelywild/ansible-collection-technitium-dns)

Ansible collection for Technitium DNS based on the [API](https://github.com/TechnitiumSoftware/DnsServer/blob/master/APIDOCS.md).


We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Communication

For more information about communication, refer to the [Ansible Communication guide](https://docs.ansible.com/ansible/devel/community/communication.html).

## Contributing to this collection

The content of this collection is made by people like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors.

Any kind of contribution is very welcome.

You don't know how to start? Refer to our [contribution guide](CONTRIBUTING.md)!

We use the following guidelines:

* [CONTRIBUTING.md](CONTRIBUTING.md)
* [REVIEW_CHECKLIST.md](REVIEW_CHECKLIST.md)
* [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html)
* [Ansible Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
* [Ansible Collection Development Guide](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections)

## Collection maintenance

The current maintainers are listed in the [MAINTAINERS](MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

To learn how to maintain / become a maintainer of this collection, refer to the [Maintainer guidelines](MAINTAINING.md).

## Governance

The process of decision making in this collection is based on discussing and finding consensus among participants.

Every voice is important. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!

## Compatibility Matrix

This collection is tested against the following Ansible and Python versions:

| Ansible Version | Python 3.10 | Python 3.11 | Python 3.12 | Python 3.13 |
|----------------|--------------|--------------|--------------|--------------|
| 2.17           | ✅           | ✅           | ✅           | ❌           |
| 2.18           | ❌           | ✅           | ✅           | ✅           |
| 2.19           | ❌           | ✅           | ✅           | ✅           |
| devel          | ❌           | ❌           | ❌           | ✅           |

**Note:** This matrix reflects our current CI testing coverage. Other combinations may work but are not regularly tested.

## Included content
See the complete list of collection content in the [Plugin Index](https://effectivelywild.github.io/ansible-collection-technitium-dns/collections/index_module.html).

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:
```bash
ansible-galaxy collection install effectivelywild.technitium_dns
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:
```yaml
---
collections:
  - name: effectivelywild.technitium_dns
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:
```bash
ansible-galaxy collection install effectivelywild.technitium_dns --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `0.1.0`:

```bash
ansible-galaxy collection install effectivelywild.technitium_dns:==0.1.0
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