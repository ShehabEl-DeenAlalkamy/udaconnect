<!-- markdownlint-configure-file {
  "MD033": false,
  "MD041": false
} -->

# Architecture Decisions

- Given the dependency graph:
  ![udaconnect dependency graph][dpendency-graph]

  `UdaConnect` can be refactored into 3 services:

  1. `udaconnect-persons-service`:

     - RESTful microservice to handle `/persons` resource including:
       - GET /persons
       - GET /persons/<person_id: int>
       - POST /persons
       - DELETE /persons/<person_id: int> (new API endpoint)

  2. `udaconnect-connections-service`:

     - RESTful microservice to handle `/connections` resource including:
       - GET /persons/<person_id: int>/connections

  3. `udaconnect-locations-service`:
     - RESTful microservice to handle `/locations` resource including:
       - GET /locations/<location_id: int>
       - POST /locations

- The proposed architecture design concludes the following:

  ![udaconnect architecture design][arch-design]

  - `UdaConnect` microservices will adopt REST APIs as the client facing interface for the following reasons:

    - REST APIs are extremely popular, widely adopted and considered as the industry defacto nowadays.
    - REST APIs provide uniform interfaces and self describing endpoints.
    - future development is more maintainable.

  - `udaconnect-connections-service` will communicate with `udaconnect-persons-service` using gRPC message passing:

    - gRPC:
      - is fast.
      - is more structured.
      - leverages HTTP/2 which means overall better security and performance.
    - PersonService GetPersons() method will be used to retrieve all the persons.
    - in the future, when the 'person' table gets crowded, gRPC will reduce the payload size since it's being serialized in binary data format.
    - since gRPC is not as widely adopted as REST APIs, it makes sense to leverage gRPC for internal microservices communication.

    - Protobuf Message:

      ```proto
      message PersonMessage {
          int32 id = 1;
          string first_name = 2;
          string last_name = 3;
          string company_name = 4;
      }

      message EmptyMessage {}

      message PersonMessageList {
          repeated PersonMessage persons = 1;
      }

      service PersonService {
          rpc GetPersons(EmptyMessage) returns (PersonMessageList);
      }
      ```

  - `udaconnect-locations-service` will leverage Kafka as a message queue passing strategy for POST /locations endpoint:

    - Location model is more complicated than Person and Connection models. creating new Location resource might take longer than expected.
    - with an asynchronous request, we can make better use of our time by doing something else instead of waiting for the server to respond.
    - this will make `UdaConnect` remain available to accept messages, more fault tolerant and reduce losing messages during downtime.
    - since POST /locations isn't expected to be much used, it makes more sense to process creating new Location resources in batches instead of on-demand.
    - Kafka needs to have 'locations' topic.

  - Since Kafka doesn't enforce the structure of the input data, Kafka will be exposed using REST Location service REST API:

    - to avoid additional resources which will increase the complexity, the Kafka producer and the consumer will be within `udaconnect-locations-service`.
    - to implement this, multi threading will be used to initialze the consumer in a separate threading module.
    - for future development purposes, Kafka producer will produce the following format:

      ```json
      {
        "action": "<action_enum: str>",
        "message": "<message: obj>"
      }
      ```

      > :memo: **Note:** this is needed for Kafka consumer to be able to handle different scenarios depending on 'action' value:

      <br />

      1. action="create":

      ```json
      {
        "action": "create",
        "message": {
          "person_id": "<person_id: int>",
          "creation_time": "<datatime_format: str>",
          "latitude": "<latitude: str>",
          "longitude": "<longitude: str>"
        }
      }
      ```

      -> Kafka consumer will call `create()` method in `Location service`.

      Response: `202 - No Content`

[dpendency-graph]: ./assets/imgs/dependency-graph-simple.png
[arch-design]: ./architecture_design.png