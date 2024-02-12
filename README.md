# RePlanIT-API

The increasing digitisation and unprecedented amount of data that is generated on a daily basis has resulted in Information and Communications Technology (ICT) devices being disposed of before the end of their functional lifetime. The result is increased ICT hardware manufacturing, which is not sustainable due to the growing demand for critical materials needed and the greenhouse emissions associated with it. A solution is to transition towards a circular economy (CE), which encourages the reuse, recycling, remanufacturing, and repurposing of materials and products. However, the technological adoption of the CE in the ICT sector is currently limited due to the the lack of standardised and findable, accessible, interoperable, reusable (FAIR) ICT data sharing between manufacturers, sustainability experts and technology provides. This paper presents the initial efforts towards an ontology, which interrelates and synchronises data sharing in the materials, ICT and CE domains. The ontology's main application is for building dynamic digital product passports of ICT devices that support FAIR ICT data sharing and sustainable human and machine decision-making.

See API doscumentation [here](https://app.swaggerhub.com/apis-docs/RePlanIT/RePlanITLaptopDPP/1.2.0).:

## Getting Started

Start your own instance of [GraphDB](https://graphdb.ontotext.com/). 

Create `.env` file by copying the `.env.example` and filling in the info of your own GraphDb instance.

Take a look at the `docker-compose.yml` file and double check that it suits your setup. If you are running GraphDB via docker on the same machine, then make sure that this docker container will be running on the same docker network.  

Start docker container using `docker compose up -d`

The API should now be hosted on `http://localhost:5052`.