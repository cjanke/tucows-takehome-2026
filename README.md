# tucows-takehome-2026
TODO

"You want Docker version 20+ and Docker Compose version 2+."


clairejanke@Claires-MacBook-Air tucows-takehome-2026 % docker --version
docker compose version
Docker version 24.0.6, build ed223bc
Docker Compose version v2.22.0-desktop.2

Using xml.etree.ElementTree for xml parsing library - it's available by default in python, and the xml is pretty similar and predictable.

the parser assumes one graph per XML file per the spec, but could be extended to support a wrapper element for multiple graphs.

`pytest tests/ -v`  to run tests

In case we want to support querying multiple graphs in the future, we store graphs in their own table and include graph ids in the records for nodes and edges. The API, though, assumes only one graph.

