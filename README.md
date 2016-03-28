# Overview

This interface layer handles the communication among Apache Spark peers.


# Usage

## Peers

This interface allows the peers of the Spark deployment to be aware of
each other. This interface layer will set the following states, as appropriate:

  * `{relation_name}.joined` A new peer in the Spark service has
  joined. The Spark charm should call `get_nodes()` to get
  a list of tuples with unit ids and IP addresses for quorum members.

    * When a unit joins the set of peers, the interface ensures there
    is no `{relation_name}.departed` state set in the conversation.

    * A call to `dismiss_joined()` will remove the `joined` state in the
    peer conversation so this charm can react to subsequent peers joining.


  * `{relation_name}.departed` A peer in the Spark service has
  departed. The Spark charm should call `get_nodes()` to get
  a list of tuples with unit ids and IP addresses for remaining quorum members.

    * When a unit leaves the set of peers, the interface ensures there
    is no `{relation_name}.joined` state set in the conversation.

    * A call to `dismiss_departed()` will remove the `departed` state in the
    peer conversation so this charm can react to subsequent peers departing.


For example, let's say that a peer is added to the Spark service
deployment. The Spark charm should handle the new peer like this:

```python
@when('spark.installed', 'sprkpeer.joined')
def quorum_add(sprkpeer):
    nodes = sprkpeer.get_nodes()
    increase_quorum(nodes)
    sprkpeer.dismiss_joined()
```

Similarly, when a peer departs:

```python
@when('spark.installed', 'sprkpeer.departed')
def quorum_remove(sprkpeer):
    nodes = sprkpeer.get_nodes()
    decrease_quorum(nodes)
    sprkpeer.dismiss_departed()
```


# Contact Information

- <bigdata@lists.ubuntu.com>
