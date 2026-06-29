# Third-Party Code

This directory contains small runtime dependencies that are vendored to keep
the public deployment path reproducible.

## `unitree_sdk2py`

Source package: Unitree SDK2 Python interface.

Why vendored:

- the deployment scripts need `unitree_sdk2py` for Go2 DDS LowState/LowCmd
  topics;
- the required subset is small enough to keep in-repo;
- this avoids forcing users to clone a separate Python SDK repository before
  running the hardware probe.

License:

```text
third_party/unitree_sdk2py/LICENSE
```

The hardware Python environment still needs the external `cyclonedds` Python
package installed.
