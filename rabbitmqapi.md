RabbitMQ Management HTTP API
Introduction
Apart from this help page, all URIs will serve only resources of type application/json, and will require HTTP basic authentication (using the standard RabbitMQ user database). The default user is guest/guest.

Many URIs require the name of a virtual host as part of the path, since names only uniquely identify objects within a virtual host. As the default virtual host is called "/", this will need to be encoded as "%2F".

PUTing a resource creates it. The JSON object you upload must have certain mandatory keys (documented below) and may have optional keys. Other keys are ignored. Missing mandatory keys constitute an error.

Since bindings do not have names or IDs in AMQP we synthesise one based on all its properties. Since predicting this name is hard in the general case, you can also create bindings by POSTing to a factory URI. See the example below.

Many URIs return lists. Such URIs can have the query string parameters sort and sort_reverse added. sort allows you to select a primary field to sort by, and sort_reverse will reverse the sort order if set to true. The sort parameter can contain subfields separated by dots. This allows you to sort by a nested component of the listed items; it does not allow you to sort by more than one field. See the example below.

You can also restrict what information is returned per item with the columns parameter. This is a comma-separated list of subfields separated by dots. See the example below.

It is possible to disable the statistics in the GET requests and obtain just the basic information of every object. This reduces considerably the amount of data returned and the memory and resource consumption of each query in the system. For some monitoring and operation purposes, these queries are more appropiate. The query string parameter disable_stats set to true will achieve this.

Most of the GET queries return many fields per object. The second part of this guide covers those.

Examples
A few quick examples for Windows and Unix, using the command line tool curl:

Get a list of vhosts:
:: Windows
C:\> curl -i -u guest:guest http://localhost:15672/api/vhosts

# Unix
$ curl -i -u guest:guest http://localhost:15672/api/vhosts

HTTP/1.1 200 OK
cache-control: no-cache
content-length: 196
content-security-policy: default-src 'self'
content-type: application/json
date: Mon, 02 Sep 2019 07:51:49 GMT
server: Cowboy
vary: accept, accept-encoding, origin

[{"cluster_state":{"rabbit@localhost":"running"},"description":"Default virtual host" ... (remainder elided)
Get a list of channels, fast publishers first, restricting the info items we get back:
:: Windows
C:\> curl -i -u guest:guest "http://localhost:15672/api/channels?sort=message_stats.publish_details.rate&sort_reverse=true&columns=name,message_stats.publish_details.rate,message_stats.deliver_get_details.rate"

# Unix
$ curl -i -u guest:guest 'http://localhost:15672/api/channels?sort=message_stats.publish_details.rate&sort_reverse=true&columns=name,message_stats.publish_details.rate,message_stats.deliver_get_details.rate'

HTTP/1.1 200 OK
cache-control: no-cache
content-length: 2
content-security-policy: default-src 'self'
content-type: application/json
date: Mon, 02 Sep 2019 07:54:35 GMT
server: Cowboy
vary: accept, accept-encoding, origin

[{"message_stats":{"publish_details":{"rate" ... (remainder elided)
Create a new vhost:
:: Windows
C:\> curl -i -u guest:guest -H "content-type:application/json" ^
      -XPUT http://localhost:15672/api/vhosts/foo

# Unix
$ curl -i -u guest:guest -H "content-type:application/json" \
   -XPUT http://localhost:15672/api/vhosts/foo

HTTP/1.1 201 Created
content-length: 0
content-security-policy: default-src 'self'
date: Mon, 02 Sep 2019 07:55:24 GMT
server: Cowboy
vary: accept, accept-encoding, origin
Note: you must specify application/json as the mime type.

Note: the name of the object is not needed in the JSON object uploaded, since it is in the URI. As a virtual host has no properties apart from its name, this means you do not need to specify a body at all!

Create a new exchange in the default virtual host:
:: Windows
C:\> curl -i -u guest:guest -H "content-type:application/json" ^
       -XPUT -d"{""type"":""direct"",""durable"":true}" ^
       http://localhost:15672/api/exchanges/%2F/my-new-exchange

# Unix
$ curl -i -u guest:guest -H "content-type:application/json" \
    -XPUT -d'{"type":"direct","durable":true}' \
    http://localhost:15672/api/exchanges/%2F/my-new-exchange

HTTP/1.1 201 Created
content-length: 0
content-security-policy: default-src 'self'
date: Mon, 02 Sep 2019 07:56:06 GMT
server: Cowboy
vary: accept, accept-encoding, origin
Note: we never return a body in response to a PUT or DELETE, unless it fails.

And delete it again:
:: Windows
C:\> curl -i -u guest:guest -H "content-type:application/json" ^
       -XDELETE http://localhost:15672/api/exchanges/%2F/my-new-exchange

# Unix
$ curl -i -u guest:guest -H "content-type:application/json" \
    -XDELETE http://localhost:15672/api/exchanges/%2F/my-new-exchange

HTTP/1.1 204 No Content
content-security-policy: default-src 'self'
date: Mon, 02 Sep 2019 07:56:59 GMT
server: Cowboy
vary: accept, accept-encoding, origin
Reference
GET	PUT	DELETE	POST	Path	Description
X				/api/overview	Various random bits of information that describe the whole system.
X	X			/api/cluster-name	Name identifying this RabbitMQ cluster.
X				/api/nodes	A list of nodes in the RabbitMQ cluster.
X				/api/nodes/name	Returns information about an individual node in the RabbitMQ cluster.
X				/api/nodes/name/memory	Returns a memory usage breakdown of an individual node in the RabbitMQ cluster.
X				/api/extensions	A list of extensions to the management plugin.
X			X	/api/definitions
/api/all-configuration (deprecated)	The server definitions - exchanges, queues, bindings, users, virtual hosts, permissions, topic permissions, and parameters. Everything apart from messages. POST to upload an existing set of definitions. Note that:
The definitions are merged. Anything already existing on the server but not in the uploaded definitions is untouched.
Conflicting definitions on immutable objects (exchanges, queues and bindings) will be ignored. The existing definition will be preserved.
Conflicting definitions on mutable objects will cause the object in the server to be overwritten with the object from the definitions.
In the event of an error you will be left with a part-applied set of definitions.
For convenience you may upload a file from a browser to this URI (i.e. you can use multipart/form-data as well as application/json) in which case the definitions should be uploaded as a form field named "file".
X			X	/api/definitions/vhost
The server definitions for a given virtual host - exchanges, queues, bindings and policies. POST to upload an existing set of definitions. Note that:
The definitions are merged. Anything already existing on the server but not in the uploaded definitions is untouched.
Conflicting definitions on immutable objects (exchanges, queues and bindings) will be ignored. The existing definition will be preserved.
Conflicting definitions on mutable objects will cause the object in the server to be overwritten with the object from the definitions.
In the event of an error you will be left with a part-applied set of definitions.
For convenience you may upload a file from a browser to this URI (i.e. you can use multipart/form-data as well as application/json) in which case the definitions should be uploaded as a form field named "file".
X				/api/connections	A list of all open connections. Use pagination parameters to filter connections.
X				/api/vhosts/vhost/connections	A list of all open connections in a specific virtual host. Use pagination parameters to filter connections.
X		X		/api/connections/name	An individual connection. DELETEing it will close the connection. Optionally set the "X-Reason" header when DELETEing to provide a reason.
X		X		/api/connections/username/username	A list of all open connections for a specific username. Use pagination parameters to filter connections. DELETEing a resource will close all the connections for a username. Optionally set the "X-Reason" header when DELETEing to provide a reason.
X				/api/connections/name/channels	List of all channels for a given connection.
X				/api/channels	A list of all open channels. Use pagination parameters to filter channels.
X				/api/vhosts/vhost/channels	A list of all open channels in a specific virtual host. Use pagination parameters to filter channels.
X				/api/channels/channel	Details about an individual channel.
X				/api/consumers	A list of all consumers.
X				/api/consumers/vhost	A list of all consumers in a given virtual host.
X				/api/exchanges	A list of all exchanges. Use pagination parameters to filter exchanges.
X				/api/exchanges/vhost	A list of all exchanges in a given virtual host. Use pagination parameters to filter exchanges.
X	X	X		/api/exchanges/vhost/name	An individual exchange. To PUT an exchange, you will need a body looking something like this:
{"type":"direct","auto_delete":false,"durable":true,"internal":false,"arguments":{}}
The type key is mandatory; other keys are optional.
When DELETEing an exchange you can add the query string parameter if-unused=true. This prevents the delete from succeeding if the exchange is bound to a queue or as a source to another exchange.

X				/api/exchanges/vhost/name/bindings/source	A list of all bindings in which a given exchange is the source.
X				/api/exchanges/vhost/name/bindings/destination	A list of all bindings in which a given exchange is the destination.
X	/api/exchanges/vhost/name/publish	Publish a message to a given exchange. You will need a body looking something like:
{"properties":{},"routing_key":"my key","payload":"my body","payload_encoding":"string"}
All keys are mandatory. The payload_encoding key should be either "string" (in which case the payload will be taken to be the UTF-8 encoding of the payload field) or "base64" (in which case the payload field is taken to be base64 encoded).
If the message is published successfully, the response will look like:
{"routed": true}
routed will be true if the message was sent to at least one queue.
Please note that the HTTP API is not ideal for high performance publishing; the need to create a new TCP connection for each message published can limit message throughput compared to AMQP or other protocols using long-lived connections.

X				/api/queues	A list of all queues. Use pagination parameters to filter queues. The parameter enable_queue_totals=true can be used in combination with the disable_stats=true parameter to return a reduced set of fields and significantly reduce the amount of data returned by this endpoint. That in turn can significantly reduce CPU and bandwidth footprint of such requests.
X				/api/queues/vhost	A list of all queues in a given virtual host. Use pagination parameters to filter queues.
X	X	X		/api/queues/vhost/name	An individual queue. To PUT a queue, you will need a body looking something like this:
{"auto_delete":false,"durable":true,"arguments":{},"node":"rabbit@smacmullen"}
All keys are optional.
When DELETEing a queue you can add the query string parameters if-empty=true and / or if-unused=true. These prevent the delete from succeeding if the queue contains messages, or has consumers, respectively.

X				/api/queues/vhost/name/bindings	A list of all bindings on a given queue.
X		/api/queues/vhost/name/contents	Contents of a queue. DELETE to purge. Note you can't GET this.
X	/api/queues/vhost/name/actions	Actions that can be taken on a queue. POST a body like:
{"action":"sync"}
Currently the actions which are supported are sync and cancel_sync.
X	/api/queues/vhost/name/get	Get messages from a queue. (This is not an HTTP GET as it will alter the state of the queue.) You should post a body looking like:
{"count":5,"ackmode":"ack_requeue_true","encoding":"auto","truncate":50000}
count controls the maximum number of messages to get. You may get fewer messages than this if the queue cannot immediately provide them.
ackmode determines whether the messages will be removed from the queue. If ackmode is ack_requeue_true or reject_requeue_true they will be requeued - if ackmode is ack_requeue_false or reject_requeue_false they will be removed.
encoding must be either "auto" (in which case the payload will be returned as a string if it is valid UTF-8, and base64 encoded otherwise), or "base64" (in which case the payload will always be base64 encoded).
If truncate is present it will truncate the message payload if it is larger than the size given (in bytes).
truncate is optional; all other keys are mandatory.

Please note that the get path in the HTTP API is intended for diagnostics etc - it does not implement reliable delivery and so should be treated as a sysadmin's tool rather than a general API for messaging.

X				/api/bindings	A list of all bindings.
X				/api/bindings/vhost	A list of all bindings in a given virtual host.
X			X	/api/bindings/vhost/e/exchange/q/queue	
A list of all bindings between an exchange and a queue. Remember, an exchange and a queue can be bound together many times!

To create a new binding, POST to this URI. Request body should be a JSON object optionally containing two fields, routing_key (a string) and arguments (a map of optional arguments):

{"routing_key":"my_routing_key", "arguments":{"x-arg": "value"}}
All keys are optional. The response will contain a Location header telling you the URI of your new binding.
X		X		/api/bindings/vhost/e/exchange/q/queue/props	An individual binding between an exchange and a queue. The props part of the URI is a "name" for the binding composed of its routing key and a hash of its arguments. props is the field named "properties_key" from a bindings listing response.
X			X	/api/bindings/vhost/e/source/e/destination	
A list of all bindings between two exchanges, similar to the list of all bindings between an exchange and a queue, above.


To create a new binding, POST to this URI. Request body should be a JSON object optionally containing two fields, routing_key (a string) and arguments (a map of optional arguments):

{"routing_key":"my_routing_key", "arguments":{"x-arg": "value"}}
All keys are optional. The response will contain a Location header telling you the URI of your new binding.
X		X		/api/bindings/vhost/e/source/e/destination/props	An individual binding between two exchanges. Similar to the individual binding between an exchange and a queue, above.
X				/api/vhosts	A list of all vhosts.
X	X	X		/api/vhosts/name	An individual virtual host. As a virtual host usually only has a name, you do not need an HTTP body when PUTing one of these. To set metadata on creation, provide a body like the following:
{"description":"virtual host description", "tags":"accounts,production"}
tags is a comma-separated list of tags. These metadata fields are optional. To enable / disable tracing, provide a body looking like:
{"tracing":true}
X				/api/vhosts/name/permissions	A list of all permissions for a given virtual host.
X				/api/vhosts/name/topic-permissions	A list of all topic permissions for a given virtual host.
X	/api/vhosts/name/start/node	Starts virtual host name on node node.
X				/api/users/	A list of all users.
X				/api/users/without-permissions	A list of users that do not have access to any virtual host.
X	/api/users/bulk-delete	Bulk deletes a list of users. Request body must contain the list:
{"users" : ["user1", "user2", "user3"]}
X	X	X		/api/users/name	An individual user. To PUT a user, you will need a body looking something like this:
{"password":"secret","tags":"administrator"}
or:
{"password_hash":"2lmoth8l4H0DViLaK9Fxi6l9ds8=", "tags":["administrator"]}
The tags key is mandatory. Either password or password_hash can be set. If neither are set the user will not be able to log in with a password, but other mechanisms like client certificates may be used. Setting password_hash to "" will ensure the user cannot use a password to log in. tags is a comma-separated list of tags for the user. Currently recognised tags are administrator, monitoring and management. password_hash must be generated using the algorithm described here. You may also specify the hash function being used by adding the hashing_algorithm key to the body. Currently recognised algorithms are rabbit_password_hashing_sha256, rabbit_password_hashing_sha512, and rabbit_password_hashing_md5.
X				/api/users/user/permissions	A list of all permissions for a given user.
X				/api/users/user/topic-permissions	A list of all topic permissions for a given user.
X				/api/user-limits	Lists per-user limits for all users.
X				/api/user-limits/user	Lists per-user limits for a specific user.
X	X		/api/user-limits/user/name	Set or delete per-user limit for user. The name URL path element refers to the name of the limit (max-connections, max-channels). Limits are set using a JSON document in the body:
{"value": 100}
. Example request:
curl -4u 'guest:guest' -H 'content-type:application/json' -X PUT localhost:15672/api/user-limits/guest/max-connections -d '{"value": 50}'
X				/api/whoami	Details of the currently authenticated user.
X				/api/permissions	A list of all permissions for all users.
X	X	X		/api/permissions/vhost/user	An individual permission of a user and virtual host. To PUT a permission, you will need a body looking something like this:
{"configure":".*","write":".*","read":".*"}
All keys are mandatory.
X				/api/topic-permissions	A list of all topic permissions for all users.
X	X	X		/api/topic-permissions/vhost/user	Topic permissions for a user and virtual host. To PUT a topic permission, you will need a body looking something like this:
{"exchange":"amq.topic","write":"^a","read":".*"}
All keys are mandatory.
X				/api/parameters	A list of all vhost-scoped parameters.
X				/api/parameters/component	A list of all vhost-scoped parameters for a given component.
X				/api/parameters/component/vhost	A list of all vhost-scoped parameters for a given component and virtual host.
X	X	X		/api/parameters/component/vhost/name	An individual vhost-scoped parameter. To PUT a parameter, you will need a body looking something like this:
{"vhost": "/","component":"federation","name":"local_username","value":"guest"}
X				/api/global-parameters	A list of all global parameters.
X	X	X		/api/global-parameters/name	An individual global parameter. To PUT a parameter, you will need a body looking something like this:
{"name":"user_vhost_mapping","value":{"guest":"/","rabbit":"warren"}}
X				/api/policies	A list of all policies.
X				/api/policies/vhost	A list of all policies in a given virtual host.
X	X	X		/api/policies/vhost/name	An individual policy. To PUT a policy, you will need a body looking something like this:
{"pattern":"^amq.", "definition": {"federation-upstream-set":"all"}, "priority":0, "apply-to": "all"}
pattern and definition are mandatory, priority and apply-to are optional.
X				/api/operator-policies	A list of all operator policy overrides.
X				/api/operator-policies/vhost	A list of all operator policy overrides in a given virtual host.
X	X	X		/api/operator-policies/vhost/name	An individual operator policy. To PUT a policy, you will need a body looking something like this:
{"pattern":"^amq.", "definition": {"expires":100}, "priority":0, "apply-to": "queues"}
pattern and definition are mandatory, priority and apply-to are optional.
X				/api/aliveness-test/vhost	Declares a test queue on the target node, then publishes and consumes a message. Intended to be used as a very basic health check. Responds a 200 OK if the check succeeded, otherwise responds with a 503 Service Unavailable.
X				/api/health/checks/alarms	Responds a 200 OK if there are no alarms in effect in the cluster, otherwise responds with a 503 Service Unavailable.
X				/api/health/checks/local-alarms	Responds a 200 OK if there are no local alarms in effect on the target node, otherwise responds with a 503 Service Unavailable.
X				/api/health/checks/certificate-expiration/within/unit	
Checks the expiration date on the certificates for every listener configured to use TLS. Responds a 200 OK if all certificates are valid (have not expired), otherwise responds with a 503 Service Unavailable.

Valid units: days, weeks, months, years. The value of the within argument is the number of units. So, when within is 2 and unit is "months", the expiration period used by the check will be the next two months.

X				/api/health/checks/port-listener/port	Responds a 200 OK if there is an active listener on the give port, otherwise responds with a 503 Service Unavailable.
X				/api/health/checks/protocol-listener/protocol	Responds a 200 OK if there is an active listener for the given protocol, otherwise responds with a 503 Service Unavailable. Valid protocol names are: amqp091, amqp10, mqtt, stomp, web-mqtt, web-stomp.
X				/api/health/checks/virtual-hosts	Responds a 200 OK if all virtual hosts and running on the target node, otherwise responds with a 503 Service Unavailable.
X				/api/health/checks/node-is-mirror-sync-critical	Checks if there are classic mirrored queues without synchronised mirrors online (queues that would potentially lose data if the target node is shut down). Responds a 200 OK if there are no such classic mirrored queues, otherwise responds with a 503 Service Unavailable.
X				/api/health/checks/node-is-quorum-critical	Checks if there are quorum queues with minimum online quorum (queues that would lose their quorum and availability if the target node is shut down). Responds a 200 OK if there are no such quorum queues, otherwise responds with a 503 Service Unavailable.
X				/api/vhost-limits	Lists per-vhost limits for all vhosts.
X				/api/vhost-limits/vhost	Lists per-vhost limits for specific vhost.
X	X		/api/vhost-limits/vhost/name	Set or delete per-vhost limit for vhost. The name URL path element refers to the name of the limit (max-connections, max-queues). Limits are set using a JSON document in the body:
{"value": 100}
. Example request:
curl -4u 'guest:guest' -H 'content-type:application/json' -X PUT localhost:15672/api/vhost-limits/my-vhost/max-connections -d '{"value": 50}'
X				/api/auth	Details about the OAuth2 configuration. It will return HTTP status 200 with body:
{"oauth_enabled":"boolean", "oauth_client_id":"string", "oauth_provider_url":"string"}
X	/api/rebalance/queues	Rebalances all queues in all vhosts. This operation is asynchronous therefore please check the RabbitMQ log file for messages regarding the success or failure of the operation.
curl -4u 'guest:guest' -XPOST localhost:15672/api/rebalance/queues/
X				/api/federation-links
/api/federation-links/vhost	Provides status for all federation links. Requires the rabbitmq_federation_management plugin to be enabled.
X		X		/api/auth/attempts/node	A list of authentication attempts.
X		X		/api/auth/attempts/node/source	A list of authentication attempts by remote address and username.
X				/api/auth/hash_password/plaintext-password	Hashes plaintext-password according to the currently configured password hashing algorithm.
X				/api/stream/connections	A list of all open stream connections. Use pagination parameters to filter connections.
Requires the rabbitmq_stream_management plugin to be enabled.
X				/api/stream/connections/vhost	A list of all open stream connections in a specific virtual host.
Requires the rabbitmq_stream_management plugin to be enabled.
X		X		/api/stream/connections/vhost/name	An individual stream connection. DELETEing it will close the stream connection. Optionally set the "X-Reason" header when DELETEing to provide a reason.
Requires the rabbitmq_stream_management plugin to be enabled.
X				/api/stream/connections/vhost/name/publishers	The list of publishers of a given stream connection.
Requires the rabbitmq_stream_management plugin to be enabled.
X				/api/stream/connections/vhost/name/consumers	The list of consumers of a given stream connection.
Requires the rabbitmq_stream_management plugin to be enabled.
X				/api/stream/publishers	The list of stream publishers.
Requires the rabbitmq_stream_management plugin to be enabled.
X				/api/stream/publishers/vhost	The list of stream publishers in a specific virtual host.
Requires the rabbitmq_stream_management plugin to be enabled.
X				/api/stream/publishers/vhost/stream	The list of stream publishers in a specific virtual host for a specific stream.
Requires the rabbitmq_stream_management plugin to be enabled.
X				/api/stream/consumers	The list of stream consumers.
Requires the rabbitmq_stream_management plugin to be enabled.
X				/api/stream/consumers/vhost	The list of stream consumers in a specific virtual host.
Requires the rabbitmq_stream_management plugin to be enabled.
HTTP API Stats
Most of the GET requests you can issue to the HTTP API return JSON objects with a large number of keys. While a few of these keys represent things you set yourself in a PUT request or AMQP command (e.g. queue durability or arguments), most of them represent statistics to do with the object in question. This page attempts to document them.

It should be read in conjunction with the manual page for rabbitmqctl (see your installation if on Unix / Linux, or the RabbitMQ website for the latest version). Any field which can be returned by a command of the form rabbitmqctl list_something will also be returned in the equivalent part of the HTTP API, so all those keys are not documented here. However, the HTTP API also adds a lot of extra fields which are not available in rabbitmqctl.

_details objects
Many fields represent a count of some kind: queue length, messages acknowledged, bytes received and so on. Such absolute counts returned by the HTTP API will often have a corresponding _details object which offers information on how this count has changed. So for example, from a queue:

    "messages": 123619,
    "messages_details": {
      "avg": 41206.333333333336,
      "avg_rate": 1030.1583333333333,
      "rate": 24723.8,
      "samples": [
        {
          "sample": 123619,
          "timestamp": 1400680560000
        },
        {
          "sample": 0,
          "timestamp": 1400680500000
        },
        {
          "sample": 0,
          "timestamp": 1400680440000
        }
      ]
    }
Here we have a messages count (the total messages in the queue), with some additional data:

avg	The average value for the requested time period (see below).
avg_rate	The average rate for the requested time period.
rate	How much the count has changed per second in the most recent sampling interval.
samples	Snapshots showing how the value has changed over the requested time period.
avg, avg_rate and samples will only appear if you request a specific time period by appending query parameters to the URL. To do this you need to set an age and an increment for the samples you want. The end of the range returned will always correspond to the present.

Different types of data take different query parameters to return samples, as in the following table. You can specify more than one set of parameters if the resource you are requesting can generate more than one type of sample (for example, queues can return message rates and queue lengths).

Messages sent and received	msg_rates_age / msg_rates_incr
Bytes sent and received	data_rates_age / data_rates_incr
Queue lengths	lengths_age / lengths_incr
Node statistics (e.g. file descriptors, disk space free)	node_stats_age / node_stats_incr
For example, appending ?lengths_age=3600&lengths_incr=60 will return the last hour's data on queue lengths, with a sample for every minute.

message_stats objects
Many objects (including queues, exchanges and channels) will return counts of messages passing through them. These are included in a message_stats object (which in turn will contain _details objects for each count, as described above).

These can contain:

publish	Count of messages published.
publish_in	Count of messages published "in" to an exchange, i.e. not taking account of routing.
publish_out	Count of messages published "out" of an exchange, i.e. taking account of routing.
confirm	Count of messages confirmed.
deliver	Count of messages delivered in acknowledgement mode to consumers.
deliver_no_ack	Count of messages delivered in no-acknowledgement mode to consumers.
get	Count of messages delivered in acknowledgement mode in response to basic.get.
get_no_ack	Count of messages delivered in no-acknowledgement mode in response to basic.get.
deliver_get	Sum of all four of the above.
redeliver	Count of subset of messages in deliver_get which had the redelivered flag set.
drop_unroutable	Count of messages dropped as unroutable.
return_unroutable	Count of messages returned to the publisher as unroutable.
Only fields for which some activity has taken place will appear.

Detailed message stats objects
In addition, queues, exchanges and channels can return a breakdown of message stats for each of their neighbours (i.e. adjacent objects in the chain: channel -> exchange -> queue -> channel). This will only happen if the rates_mode configuration item has been switched to detailed from its default of basic.

As this possibly constitutes a large quantity of data, it is also only returned when querying a single channel, queue or exchange rather than a list. Note also that the default sample retention policy means that these detailed message stats do not retain historical data for more than a few seconds.

The detailed message stats objects have different names depending on where they are (documented below). Each set of detailed stats consists of a list of objects with two fields, one identifying the partner object and one stats which is a message_stats object as described above.

For example, from a queue:

  "incoming": [
    {
      "stats": {
        "publish": 352593,
        "publish_details": {
          "rate": 100.2
        }
      },
      "exchange": {
        "name": "my-exchange",
        "vhost": "/"
      }
    }
    {
      "stats": {
        "publish": 543784,
        "publish_details": {
          "rate": 54.6
        }
      },
      "exchange": {
        "name": "amq.topic",
        "vhost": "/"
      }
    }
  ],
This queue is currently receiving messages from two exchanges: 100.2 msg/s from "my-exchange" and 54.6 msg/s from "amq.topic".

/api/overview
This has the following fields:

cluster_name	The name of the entire cluster, as set with rabbitmqctl set_cluster_name.
contexts	A list of web application contexts in the cluster.
erlang_full_version	A string with extended detail about the Erlang VM and how it was compiled, for the node connected to.
erlang_version	A string with the Erlang version of the node connected to. As clusters should all run the same version this can be taken as representing the cluster.
exchange_types	A list of all exchange types available.
listeners	All (non-HTTP) network listeners for all nodes in the cluster. (See contexts in /api/nodes for HTTP).
management_version	Version of the management plugin in use.
message_stats	A message_stats object for everything the user can see - for all vhosts regardless of permissions in the case of monitoring and administrator users, and for all vhosts the user has access to for other users.
node	The name of the cluster node this management plugin instance is running on.
object_totals	An object containing global counts of all connections, channels, exchanges, queues and consumers, subject to the same visibility rules as for message_stats.
queue_totals	An object containing sums of the messages, messages_ready and messages_unacknowledged fields for all queues, again subject to the same visibility rules as for message_stats.
rabbitmq_version	Version of RabbitMQ on the node which processed this request.
rates_mode	'none', 'basic' or 'detailed'.
statistics_db_event_queue	Number of outstanding statistics events yet to be processed by the database.
statistics_db_node	Name of the cluster node hosting the management statistics database.
/api/nodes
This has the following fields:

applications	List of all Erlang applications running on the node.
auth_mechanisms	List of all SASL authentication mechanisms installed on the node.
cluster_links	A list of the other nodes in the cluster. For each node, there are details of the TCP connection used to connect to it and statistics on data that has been transferred.
config_files	List of config files read by the node.
contexts	List of all HTTP listeners on the node.
db_dir	Location of the persistent storage used by the node.
disk_free	Disk free space in bytes.
disk_free_alarm	Whether the disk alarm has gone off.
disk_free_limit	Point at which the disk alarm will go off.
enabled_plugins	List of plugins which are both explicitly enabled and running.
exchange_types	Exchange types available on the node.
fd_total	File descriptors available.
fd_used	Used file descriptors.
io_read_avg_time	Average wall time (milliseconds) for each disk read operation in the last statistics interval.
io_read_bytes	Total number of bytes read from disk by the persister.
io_read_count	Total number of read operations by the persister.
io_reopen_count	Total number of times the persister has needed to recycle file handles between queues. In an ideal world this number will be zero; if the number is large, performance might be improved by increasing the number of file handles available to RabbitMQ.
io_seek_avg_time	Average wall time (milliseconds) for each seek operation in the last statistics interval.
io_seek_count	Total number of seek operations by the persister.
io_sync_avg_time	Average wall time (milliseconds) for each fsync() operation in the last statistics interval.
io_sync_count	Total number of fsync() operations by the persister.
io_write_avg_time	Average wall time (milliseconds) for each disk write operation in the last statistics interval.
io_write_bytes	Total number of bytes written to disk by the persister.
io_write_count	Total number of write operations by the persister.
log_files	List of log files used by the node. If the node also sends messages to stdout, "<stdout>" is also reported in the list.
mem_used	Memory used in bytes.
mem_alarm	Whether the memory alarm has gone off.
mem_limit	Point at which the memory alarm will go off.
mnesia_disk_tx_count	Number of Mnesia transactions which have been performed that required writes to disk. (e.g. creating a durable queue). Only transactions which originated on this node are included.
mnesia_ram_tx_count	Number of Mnesia transactions which have been performed that did not require writes to disk. (e.g. creating a transient queue). Only transactions which originated on this node are included.
msg_store_read_count	Number of messages which have been read from the message store.
msg_store_write_count	Number of messages which have been written to the message store.
name	Node name.
net_ticktime	Current kernel net_ticktime setting for the node.
os_pid	Process identifier for the Operating System under which this node is running.
partitions	List of network partitions this node is seeing.
proc_total	Maximum number of Erlang processes.
proc_used	Number of Erlang processes in use.
processors	Number of cores detected and usable by Erlang.
queue_index_journal_write_count	Number of records written to the queue index journal. Each record represents a message being published to a queue, being delivered from a queue, and being acknowledged in a queue.
queue_index_read_count	Number of records read from the queue index.
queue_index_write_count	Number of records written to the queue index.
rates_mode	'none', 'basic' or 'detailed'.
run_queue	Average number of Erlang processes waiting to run.
running	Boolean for whether this node is up. Obviously if this is false, most other stats will be missing.
sasl_log_file	Location of sasl log file.
sockets_total	File descriptors available for use as sockets.
sockets_used	File descriptors used as sockets.
type	'disc' or 'ram'.
uptime	Time since the Erlang VM started, in milliseconds.
/api/nodes/(name)
All of the above, plus:

memory	Detailed memory use statistics. Only appears if ?memory=true is appended to the URL.
binary	Detailed breakdown of the owners of binary memory. Only appears if ?binary=true is appended to the URL. Note that this can be an expensive query if there are many small binaries in the system.
/api/connections
/api/connections/(name)
See documentation for rabbitmqctl list_connections. No additional fields, although pid is replaced by node.

Note also that while non-AMQP connections will appear in this list (unlike rabbitmqctl list_connections), they will omit many of the connection-level statistics.

/api/connections/(name)/channels
/api/channels
See documentation for rabbitmqctl list_channels, with pid replaced by node, plus:

connection_details	Some basic details about the owning connection.
message_stats	See the section on message_stats above.
/api/channels/(name)
All the above, plus

publishes	Detailed message stats (see section above) for publishes to exchanges.
deliveries	Detailed message stats for deliveries from queues.
consumer_details	List of consumers on this channel, with some details on each.
/api/exchanges
/api/exchanges/(vhost)
See documentation for rabbitmqctl list_exchanges, plus:

message_stats	See the section on message_stats above.
/api/exchanges/(vhost)/(name)
All the above, plus:

incoming	Detailed message stats (see section above) for publishes from channels into this exchange.
outgoing	Detailed message stats for publishes from this exchange into queues.
/api/queues
When using the query parameters combination of disable_stats and enable_queue_totals this query returns the following fields:
name	The name of the queue.
vhost	The name of the virtual host.
type	The type of the queue.
node	Depending on the type of the queue, this is the node which holds the queue or hosts the leader.
state	The status of the queue.
arguments	The arguments of the queue.
auto_delete	The value of the auto_delete argument.
durable	The value of the durable argument.
exclusive	The value of the exclusive argument.
messages	The total number of messages in the queue.
messages_ready	The number of messages ready to be delivered in the queue.
messages_unacknowledged	The number of messages waiting for acknowledgement in the queue.
/api/queues/(vhost)
See documentation for rabbitmqctl list_queues, with all references to pids replaced by nodes plus:

message_stats	See the section on message_stats above.
/api/queues/(vhost)/(name)
All the above, plus:

incoming	Detailed message stats (see section above) for publishes from exchanges into this queue.
deliveries	Detailed message stats for deliveries from this queue into channels.
consumer_details	List of consumers on this channel, with some details on each.
/api/vhosts/
/api/vhosts/(name)
All the fields from rabbitmqctl list_vhosts (i.e. name and tracing) plus:

message_stats	Global message_stats for this vhost. Note that activity for other users in this vhost is shown, even for users without the monitoring tag.
messages messages_ready messages_acknowledged	Sum of these fields for all queues in the vhost.
recv_oct send_oct	Sum of these fields for all connections to the vhost.
Pagination Parameters
The pagination can be applied to the endpoints that list
queues
exchanges
connections
channels
Below are the query parameters that can be used.

Parameter NameData TypeDescription
page	Positive integer	Page number
page_size	Positive integer	Number of elements for page (default value: 100)
name	String	Filter by name, for example queue name, exchange name etc..
use_regex	Boolean	Enables regular expression for the param name
Examples:

http://localhost:15672/api/queues?page=1&page_size=50	Fetches the first queue page with 50 elements
http://localhost:15672/api/queues/my-vhost?page=1&page_size=100&name=&use_regex=false&pagination=true	Filter the first queues page for the virtual host "my-vhost"
http://localhost:15672/api/exchanges?page=1&page_size=100&name=%5Eamq&use_regex=true&pagination=true	Filter the first exchanges page, 100 elements, with named filtered using the regular expression "^amq"
