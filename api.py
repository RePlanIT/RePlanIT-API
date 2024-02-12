from flask import Flask
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask import request
from SPARQLWrapper import SPARQLWrapper, JSON
from dotenv import load_dotenv
import os
import json

app = Flask(__name__)
CORS(app)

# load the env variables
load_dotenv() 
username = os.getenv('username')
password = os.getenv('password')
graphdb_url = os.getenv('graphdb_url')

# /AllLaptopDPPs&limit=50
# Returns all laptop DPP.
@app.route('/AllLaptopDPPs')
def get_laptops():
    # get the limit variable if it is present in the URL parameters
    # and prepare the string for the query
    limit = request.args.get('limit')
    limit_string = ""
    if limit is None:
        limit_string = ""
    else:
        limit_string = "limit %s" % (limit)

    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
        PREFIX : <http://www.semanticweb.org/RePlanIT/>
        prefix onto:<http://www.ontotext.com/> 
        select * where
        { ?ICTDevice a :Laptop;
            :hasBrand ?Brand;
            :Model ?Model;
            :ModelYear ?ModelYear;
            :hasStatus ?Status;
            :Image ?Image.
        } %s 
    """ % (limit_string)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    results_temp = []
    laptop_ids = []
    # reformat some of the strings for better readability
    for laptop in results['results']['bindings']:
        laptop_id = laptop['ICTDevice']['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        if laptop_id not in laptop_ids:
            laptop_ids.append(laptop_id)
            laptop_summary = {
                "id" :  laptop_id,
            }
            for var in vars:
                laptop_summary[var] = laptop[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
            results_temp.append(laptop_summary)
    return results_temp

# /LaptopDPP/{id}
# Returns a laptop's DPP.
@app.route('/LaptopDPP/<id>')
def get_laptop(id):
    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
        PREFIX : <http://www.semanticweb.org/RePlanIT/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX unit: <https://qudt.org/2.1/vocab/>
        PREFIX om-2: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
        PREFIX dpv: <http://www.w3.org/ns/dpv#>
        select * where { 
            ?LaptopID a :Laptop;
                :AssemblyNumber ?AssemblyNumber;
                :hasBrand ?Brand;
                :Model ?Model;
                :ModelYear ?ModelYear;
                :hasStatus ?Status;
                :DeliveryTime ?DeliveryTime;
                :ICTDeviceWeight ?Weight;
                :hasCertification ?Certification;
                :hasDeclarationType ?Declaration;
                :DeclarationDate ?DeclarationDate;
                :PurchaseCostValue ?PurchaseCost;
                :CurrentCostValue ?CurrentCost;                          
                :MaintenanceCycles ?MaintenanceCycles;
                :hasSupport ?Support;
                :SupportCostValue ?SupportCost;
                :hasOperatingSystem ?OperatingSystem;
                :hasSecuritySoftware ?SecuritySoftware;
                :WarrantyDuration ?WarrantyDuration;
                :Image ?Image;
                :hasComponent ?Component;
                :DisplayResolution ?DisplayResolution;
                :ScreenSize ?ScreenSize;                             
                :hasGraphicsCardProcessor ?GraphicsCardProcessor;
                :ClockRate ?Clockrate;
                :CameraPixels ?CameraPixels;
                :hasMemory ?Memory;
                :RAMSize ?RAM;
                :ROMSize ?ROM;
                :BatteryCapacity ?BatteryCapacity;
                :BatteryLifetime ?BatteryLifetime;
                :BatteryWeight   ?BatteryWeight;                      
                :hasCPUSeries ?CPU;
                :CPULoad ?CPULoad;
                :CPUSpeed ?CPUSpeed;
                :hasSensor ?Sensor;
                :CarbonFootprintUse ?CarbonFootprintUse;
                :CarbonFootprintDistribution ?CarbonFootprintDistribution;
                :CarbonFootprintErrorratio ?CarbonFootprintErrorratio;
                :CarbonFootprintEoL ?CarbonFootprintEoL;
                :CarbonFootprintManufacturing ?CarbonFootprintManufacturing;
                :CarbonFootprint_kg_Use ?CarbonFootprint_kg_Use;
                :CarbonFootprint_kg_Distribution ?CarbonFootprint_kg_Distribution;
                :CarbonFootprint_kg_EoL ?CarbonFootprint_kg_EoL;
                :CarbonFootprint_kg_Manufacturing ?CarbonFootprint_kg_Manufacturing;
                :CircularActivityCost ?CircularActivityCost;
                :DeviceCarbonFootprint ?DeviceCarbonFootprint;
                :DeviceCarbonFootprintErrorRatio ?DeviceCarbonFootprintErrorRatio;
                :EnergyConsumption ?EnergyConsumption;
                :EPDAvailability  ?EPDAvailability;
                :SourceHash ?SourceHash;
                :EPDSource ?EPDSource;
                :EPDDeviceLifetime ?EPDDeviceLifetime;
                :EPDDeviceWeight ?EPDDeviceWeight;
                :EPDUseLocation ?EPDUseLocation;
                :EPDFinalManufacturingLocation ?EPDFinalManufacturingLocation;
                :EPDUseEnergyDemand ?EPDUseEnergyDemand;
                :GHGCostProduction ?GHGCostProduction;
                :GHGCostUse ?GHGCostUse;
                :CarbonFootprintSource ?CarbonFootprintSource;
                :ProductSpecificationSource ?ProductSpecificationSource;
                :MaterialCompositionSource  ?MaterialCompositionSource;
                :MaterialRecyclability ?MaterialRecyclability;
                :AluminiumWeight ?AluminiumWeight;                   
                :CopperWeight ?CopperWeight;
                :SteelWeight ?SteelWeight;                                      
                :PlasticWeight ?PlasticWeight;
                :PCBWeight ?PCBWeight;
                :GlassesWeight ?GlassesWeight;
                :OtherMaterialsWeight ?OtherMaterialsWeight;
                :OtherMetalsWeight ?OtherMetalsWeight;
                :Waste ?Waste;
                :RecycledContent ?RecycledContent;
                
                :CollectionRateValue ?CollectionRateValue;
                :EoLRefurbishmentRate ?EoLRefurbishmentRate;
                :EoLRemanufacturingAluminium ?EoLRemanufacturingAluminium;                  
                :EoLRemanufacturingCopper ?EoLRemanufacturingCopper;                  
                :EoLRemanufacturingSteel ?EoLRemanufacturingSteel;                  
                :EoLRemanufacturingBattery ?EoLRemanufacturingBattery;                  
                :EoLRemanufacturingPCB ?EoLRemanufacturingPCB;                  
                :EoLRemanufacturingPlastic ?EoLRemanufacturingPlastic;                  
                :EoLRemanufacturingGlasses ?EoLRemanufacturingGlasses ;                  
                :EoLRemanufacturingOtherMaterials ?EoLRemanufacturingOtherMaterials;           
                :EoLRemanufacturingOtherMetals ?EoLRemanufacturingOtherMetals;
                
                :EoLRecycledCLAluminium ?EoLRecycledCLAluminium;
                :EoLRecycledCLCopper ?EoLRecycledCLCopper;
                :EoLRecycledCLSteel ?EoLRecycledCLSteel;
                :EoLRecycledCLBattery ?EoLRecycledCLBattery;
                :EoLRecycledCLGlasses ?EoLRecycledCLGlasses;
                :EoLRecycledCLPCB ?EoLRecycledCLPCB;
                :EoLRecycledCLPlastic ?EoLRecycledCLPlastic;
                :EoLRecycledCLOtherMetals ?EoLRecycledCLOtherMetals;
                :EoLRecycledCLOtherMaterials ?EoLRecycledCLOtherMaterials;
                
                :EoLRecycledOLAluminium ?EoLRecycledOLAluminium;
                :EoLRecycledOLCopper ?EoLRecycledOLCopper;
                :EoLRecycledOLSteel ?EoLRecycledOLSteel;
                :EoLRecycledOLBattery ?EoLRecycledOLBattery;
                :EoLRecycledOLGlasses ?EoLRecycledOLGlasses;
                :EoLRecycledOLPCB ?EoLRecycledOLPCB;
                :EoLRecycledOLPlastic ?EoLRecycledOLPlastic;
                :EoLRecycledOLOtherMetals ?EoLRecycledOLOtherMetals ;
                :EoLRecycledOLOtherMaterials ?EoLRecycledOLOtherMaterials.
        ?Agent :isResponsibleFor ?LaptopID;
                dpv:hasRole ?Role;
                :Email ?Email;
                :TelephoneNumber ?TelephoneNumber;
                :worksFor ?Company.
        FILTER(?LaptopID=:%s). 
        } limit 1
    """ % (id)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    laptop_summary = {}
    # reformat some of the strings for better readability
    for laptop in results['results']['bindings']:
        laptop_id = id
        for var in vars:
            laptop_summary[var] = laptop[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        laptop_summary['id'] = laptop_id
    return laptop_summary

# /NewLaptopDPP/{id}
# Returns a new laptop's DPP
@app.route('/NewLaptopDPP/<id>')
def get_newlaptop(id):
    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
        PREFIX : <http://www.semanticweb.org/RePlanIT/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX unit: <https://qudt.org/2.1/vocab/>
        PREFIX om-2: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
        PREFIX dpv: <http://www.w3.org/ns/dpv#>
        select * where { 
            ?LaptopID a :Laptop;
                :AssemblyNumber ?AssemblyNumber;
                :hasBrand ?Brand;
                :Model ?Model;
                :ModelYear ?ModelYear;
                :hasStatus ?Status;
                :DeliveryTime ?DeliveryTime;
                :ICTDeviceWeight ?Weight;
                :hasCertification ?Certification;
                :hasDeclarationType ?Declaration;
                :DeclarationDate ?DeclarationDate;
                :PurchaseCostValue ?PurchaseCost;
                :CurrentCostValue ?CurrentCost;                          
                :MaintenanceCycles ?MaintenanceCycles;
                :hasSupport ?Support;
                :SupportCostValue ?SupportCost;
                :hasOperatingSystem ?OperatingSystem;
                :hasSecuritySoftware ?SecuritySoftware;
                :WarrantyDuration ?WarrantyDuration;
                :Image ?Image;
                :hasComponent ?Component;
                :DisplayResolution ?DisplayResolution;
                :ScreenSize ?ScreenSize;                             
                :hasGraphicsCardProcessor ?GraphicsCardProcessor;
                :ClockRate ?Clockrate;
                :CameraPixels ?CameraPixels;
                :hasMemory ?Memory;
                :RAMSize ?RAM;
                :ROMSize ?ROM;
                :BatteryCapacity ?BatteryCapacity;
                :BatteryLifetime ?BatteryLifetime;
                :BatteryWeight   ?BatteryWeight;                      
                :hasCPUSeries ?CPU;
                :CPULoad ?CPULoad;
                :CPUSpeed ?CPUSpeed;
                :hasSensor ?Sensor;
                :CarbonFootprintUse ?CarbonFootprintUse;
                :CarbonFootprintDistribution ?CarbonFootprintDistribution;
                :CarbonFootprintEoL ?CarbonFootprintEoL;
                :CarbonFootprintManufacturing ?CarbonFootprintManufacturing;
                :CarbonFootprint_kg_Use ?CarbonFootprint_kg_Use;
                :CarbonFootprint_kg_Distribution ?CarbonFootprint_kg_Distribution;
                :CarbonFootprint_kg_EoL ?CarbonFootprint_kg_EoL;
                :CarbonFootprint_kg_Manufacturing ?CarbonFootprint_kg_Manufacturing;
                :CircularActivityCost ?CircularActivityCost;
                :DeviceCarbonFootprint ?DeviceCarbonFootprint;
                :DeviceCarbonFootprintErrorRatio ?DeviceCarbonFootprintErrorRatio;
                :EnergyConsumption ?EnergyConsumption;
                :EPDAvailability  ?EPDAvailability;
                :SourceHash ?SourceHash;
                :EPDSource ?EPDSource;
                :EPDDeviceLifetime ?EPDDeviceLifetime;
                :EPDDeviceWeight ?EPDDeviceWeight;
                :EPDUseLocation ?EPDUseLocation;
                :EPDFinalManufacturingLocation ?EPDFinalManufacturingLocation;
                :EPDUseEnergyDemand ?EPDUseEnergyDemand;
                :GHGCostProduction ?GHGCostProduction;
                :GHGCostUse ?GHGCostUse;
                :CarbonFootprintSource ?CarbonFootprintSource;
                :ProductSpecificationSource ?ProductSpecificationSource;
                :MaterialCompositionSource  ?MaterialCompositionSource;
                :MaterialRecyclability ?MaterialRecyclability;
                :AluminiumWeight ?AluminiumWeight;                   
                :CopperWeight ?CopperWeight;
                :SteelWeight ?SteelWeight;                                      
                :PlasticWeight ?PlasticWeight;
                :PCBWeight ?PCBWeight;
                :GlassesWeight ?GlassesWeight;
                :OtherMaterialsWeight ?OtherMaterialsWeight;
                :OtherMetalsWeight ?OtherMetalsWeight;
                :Waste ?Waste;
                :RecycledContent ?RecycledContent;
                
                :CollectionRateValue ?CollectionRateValue;
                :EoLRefurbishmentRate ?EoLRefurbishmentRate;
                :EoLRemanufacturingAluminium ?EoLRemanufacturingAluminium;                  
                :EoLRemanufacturingCopper ?EoLRemanufacturingCopper;                  
                :EoLRemanufacturingSteel ?EoLRemanufacturingSteel;                  
                :EoLRemanufacturingBattery ?EoLRemanufacturingBattery;                  
                :EoLRemanufacturingPCB ?EoLRemanufacturingPCB;                  
                :EoLRemanufacturingPlastic ?EoLRemanufacturingPlastic;                  
                :EoLRemanufacturingGlasses ?EoLRemanufacturingGlasses ;                  
                :EoLRemanufacturingOtherMaterials ?EoLRemanufacturingOtherMaterials;           
                :EoLRemanufacturingOtherMetals ?EoLRemanufacturingOtherMetals;
                
                :EoLRecycledCLAluminium ?EoLRecycledCLAluminium;
                :EoLRecycledCLCopper ?EoLRecycledCLCopper;
                :EoLRecycledCLSteel ?EoLRecycledCLSteel;
                :EoLRecycledCLBattery ?EoLRecycledCLBattery;
                :EoLRecycledCLGlasses ?EoLRecycledCLGlasses;
                :EoLRecycledCLPCB ?EoLRecycledCLPCB;
                :EoLRecycledCLPlastic ?EoLRecycledCLPlastic;
                :EoLRecycledCLOtherMetals ?EoLRecycledCLOtherMetals;
                :EoLRecycledCLOtherMaterials ?EoLRecycledCLOtherMaterials;
                
                :EoLRecycledOLAluminium ?EoLRecycledOLAluminium;
                :EoLRecycledOLCopper ?EoLRecycledOLCopper;
                :EoLRecycledOLSteel ?EoLRecycledOLSteel;
                :EoLRecycledOLBattery ?EoLRecycledOLBattery;
                :EoLRecycledOLGlasses ?EoLRecycledOLGlasses;
                :EoLRecycledOLPCB ?EoLRecycledOLPCB;
                :EoLRecycledOLPlastic ?EoLRecycledOLPlastic;
                :EoLRecycledOLOtherMetals ?EoLRecycledOLOtherMetals ;
                :EoLRecycledOLOtherMaterials ?EoLRecycledOLOtherMaterials.
        ?Agent :isResponsibleFor ?LaptopID;
                dpv:hasRole ?Role;
                :Email ?Email;
                :TelephoneNumber ?TelephoneNumber;
                :worksFor ?Company.
        FILTER(?LaptopID=:%s). 
        FILTER(?Status=:New). 
        OPTIONAL {
        ?ICTDevice a :Laptop;
            :CarbonFootprintErrorratio ?CarbonFootprintErrorratio.
        }
        OPTIONAL {
            ?ICTDevice a :Laptop;
                :CarbonFootprintErrorRatio ?CarbonFootprintErrorRatio.
        }
        } limit 1
    """ % (id)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    laptop_summary = {}
    # reformat some of the strings for better readability
    for laptop in results['results']['bindings']:
        laptop_id = id
        for var in vars:
            if var in laptop:
                laptop_summary[var] = laptop[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        laptop_summary['id'] = laptop_id
    return laptop_summary

# /RepairedLaptopDPP/{id}
# Returns a repaired laptop's DPP.
@app.route('/RepairedLaptopDPP/<id>')
def get_repairedlaptop(id):
    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
    PREFIX : <http://www.semanticweb.org/RePlanIT/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX unit: <https://qudt.org/2.1/vocab/>
    PREFIX om-2: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    PREFIX dpv: <http://www.w3.org/ns/dpv#>
    select * where { 
        ?LaptopID a :Laptop;
            :AssemblyNumber ?AssemblyNumber;
            :hasBrand ?Brand;
            :Model ?Model;
            :ModelYear ?ModelYear;
            :hasStatus ?Status;
            :DeliveryTime ?DeliveryTime;
            :ICTDeviceWeight ?Weight;
            :hasCertification ?Certification;
            :hasDeclarationType ?Declaration;
            :DeclarationDate ?DeclarationDate;
            :PurchaseCostValue ?PurchaseCost;
            :CurrentCostValue ?CurrentCost;                          
            :MaintenanceCycles ?MaintenanceCycles;
            :hasSupport ?Support;
            :SupportCostValue ?SupportCost;
            :hasOperatingSystem ?OperatingSystem;
            :hasSecuritySoftware ?SecuritySoftware;
            :WarrantyDuration ?WarrantyDuration;
            :Image ?Image;
            :hasComponent ?Component;
            :DisplayResolution ?DisplayResolution;
            :ScreenSize ?ScreenSize;                             
            :hasGraphicsCardProcessor ?GraphicsCardProcessor;
            :ClockRate ?Clockrate;
            :CameraPixels ?CameraPixels;
            :hasMemory ?Memory;
            :RAMSize ?RAM;
            :ROMSize ?ROM;
            :BatteryCapacity ?BatteryCapacity;
            :BatteryLifetime ?BatteryLifetime;
            :BatteryWeight   ?BatteryWeight;                      
            :hasCPUSeries ?CPU;
            :CPULoad ?CPULoad;
            :CPUSpeed ?CPUSpeed;
            :hasSensor ?Sensor;
            :CarbonFootprintUse ?CarbonFootprintUse;
            :CarbonFootprintDistribution ?CarbonFootprintDistribution;
            :CarbonFootprintErrorratio ?CarbonFootprintErrorratio;
            :CarbonFootprintEoL ?CarbonFootprintEoL;
            :CarbonFootprintManufacturing ?CarbonFootprintManufacturing;
            :CarbonFootprint_kg_Use ?CarbonFootprint_kg_Use;
            :CarbonFootprint_kg_Distribution ?CarbonFootprint_kg_Distribution;
            :CarbonFootprint_kg_EoL ?CarbonFootprint_kg_EoL;
            :CarbonFootprint_kg_Manufacturing ?CarbonFootprint_kg_Manufacturing;
            :CircularActivityCost ?CircularActivityCost;
            :DeviceCarbonFootprint ?DeviceCarbonFootprint;
            :DeviceCarbonFootprintErrorRatio ?DeviceCarbonFootprintErrorRatio;
            :EnergyConsumption ?EnergyConsumption;
            :EPDAvailability  ?EPDAvailability;
            :SourceHash ?SourceHash;
            :EPDSource ?EPDSource;
            :EPDDeviceLifetime ?EPDDeviceLifetime;
            :EPDDeviceWeight ?EPDDeviceWeight;
            :EPDUseLocation ?EPDUseLocation;
            :EPDFinalManufacturingLocation ?EPDFinalManufacturingLocation;
            :EPDUseEnergyDemand ?EPDUseEnergyDemand;
            :GHGCostProduction ?GHGCostProduction;
            :GHGCostUse ?GHGCostUse;
            :CarbonFootprintSource ?CarbonFootprintSource;
            :ProductSpecificationSource ?ProductSpecificationSource;
            :MaterialCompositionSource  ?MaterialCompositionSource;
            :MaterialRecyclability ?MaterialRecyclability;
            :AluminiumWeight ?AluminiumWeight;                   
            :CopperWeight ?CopperWeight;
            :SteelWeight ?SteelWeight;                                      
            :PlasticWeight ?PlasticWeight;
            :PCBWeight ?PCBWeight;
            :GlassesWeight ?GlassesWeight;
            :OtherMaterialsWeight ?OtherMaterialsWeight;
            :OtherMetalsWeight ?OtherMetalsWeight;
            :Waste ?Waste;
            :RecycledContent ?RecycledContent;
            
            :CollectionRateValue ?CollectionRateValue;
            :EoLRefurbishmentRate ?EoLRefurbishmentRate;    
            :EoLRemanufacturingAluminium ?EoLRemanufacturingAluminium;                  
            :EoLRemanufacturingCopper ?EoLRemanufacturingCopper;                  
            :EoLRemanufacturingSteel ?EoLRemanufacturingSteel;                  
            :EoLRemanufacturingBattery ?EoLRemanufacturingBattery;                  
            :EoLRemanufacturingPCB ?EoLRemanufacturingPCB;                  
            :EoLRemanufacturingPlastic ?EoLRemanufacturingPlastic;                  
            :EoLRemanufacturingGlasses ?EoLRemanufacturingGlasses ;                  
            :EoLRemanufacturingOtherMaterials ?EoLRemanufacturingOtherMaterials;           
            :EoLRemanufacturingOtherMetals ?EoLRemanufacturingOtherMetals;
            
            :EoLRecycledCLAluminium ?EoLRecycledCLAluminium;
            :EoLRecycledCLCopper ?EoLRecycledCLCopper;
            :EoLRecycledCLSteel ?EoLRecycledCLSteel;
            :EoLRecycledCLBattery ?EoLRecycledCLBattery;
            :EoLRecycledCLGlasses ?EoLRecycledCLGlasses;
            :EoLRecycledCLPCB ?EoLRecycledCLPCB;
            :EoLRecycledCLPlastic ?EoLRecycledCLPlastic;
            :EoLRecycledCLOtherMetals ?EoLRecycledCLOtherMetals;
            :EoLRecycledCLOtherMaterials ?EoLRecycledCLOtherMaterials;
        
            :EoLRecycledOLAluminium ?EoLRecycledOLAluminium;
            :EoLRecycledOLCopper ?EoLRecycledOLCopper;
            :EoLRecycledOLSteel ?EoLRecycledOLSteel;
            :EoLRecycledOLBattery ?EoLRecycledOLBattery;
            :EoLRecycledOLGlasses ?EoLRecycledOLGlasses;
            :EoLRecycledOLPCB ?EoLRecycledOLPCB;
            :EoLRecycledOLPlastic ?EoLRecycledOLPlastic;
            :EoLRecycledOLOtherMetals ?EoLRecycledOLOtherMetals ;
            :EoLRecycledOLOtherMaterials ?EoLRecycledOLOtherMaterials.
            ?CircularStrategy :isSelectedCircularStrategyFor ?LaptopID;
                        :dueToReason ?Reason;
                        :startDate ?StartDate;
                        :endDate ?EndDate;
                        :hasStatus ?ProcessStatus.                                                     
        ?Agent :isResponsibleFor ?LaptopID;
                dpv:hasRole ?Role;
                :Email ?Email;
                :TelephoneNumber ?TelephoneNumber;
                :worksFor ?Company.
        FILTER(?LaptopID=:%s). 
        FILTER(?Status=:Repaired). 
        }limit 1
    """ % (id)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    laptop_summary = {}
    # reformat some of the strings for better readability
    for laptop in results['results']['bindings']:
        laptop_id = id
        for var in vars:
            laptop_summary[var] = laptop[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        laptop_summary['id'] = laptop_id
    return laptop_summary

# /RefurbushedLaptopDPP/{id}
# Returns a repaired laptop's DPP.
@app.route('/RefurbishedLaptopDPP/<id>')
def get_refurbishedlaptop(id):
    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
    PREFIX : <http://www.semanticweb.org/RePlanIT/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX unit: <https://qudt.org/2.1/vocab/>
    PREFIX om-2: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    PREFIX dpv: <http://www.w3.org/ns/dpv#>
    select * where { 
        ?LaptopID a :Laptop;
            :AssemblyNumber ?AssemblyNumber;
            :hasBrand ?Brand;
            :Model ?Model;
            :ModelYear ?ModelYear;
            :hasStatus ?Status;
            :DeliveryTime ?DeliveryTime;
            :ICTDeviceWeight ?Weight;
            :hasCertification ?Certification;
            :hasDeclarationType ?Declaration;
            :DeclarationDate ?DeclarationDate;
            :PurchaseCostValue ?PurchaseCost;
            :CurrentCostValue ?CurrentCost;                          
            :MaintenanceCycles ?MaintenanceCycles;
            :hasSupport ?Support;
            :SupportCostValue ?SupportCost;
            :hasOperatingSystem ?OperatingSystem;
            :hasSecuritySoftware ?SecuritySoftware;
            :WarrantyDuration ?WarrantyDuration;
            :Image ?Image;
            :hasComponent ?Component;
            :DisplayResolution ?DisplayResolution;
            :ScreenSize ?ScreenSize;                             
            :hasGraphicsCardProcessor ?GraphicsCardProcessor;
            :ClockRate ?Clockrate;
            :CameraPixels ?CameraPixels;
            :hasMemory ?Memory;
            :RAMSize ?RAM;
            :ROMSize ?ROM;
            :BatteryCapacity ?BatteryCapacity;
            :BatteryLifetime ?BatteryLifetime;
            :BatteryWeight   ?BatteryWeight;                      
            :hasCPUSeries ?CPU;
            :CPULoad ?CPULoad;
            :CPUSpeed ?CPUSpeed;
            :hasSensor ?Sensor;
            :CarbonFootprintUse ?CarbonFootprintUse;
            :CarbonFootprintDistribution ?CarbonFootprintDistribution;
            :CarbonFootprintErrorratio ?CarbonFootprintErrorratio;
            :CarbonFootprintEoL ?CarbonFootprintEoL;
            :CarbonFootprintManufacturing ?CarbonFootprintManufacturing;
            :CarbonFootprint_kg_Use ?CarbonFootprint_kg_Use;
            :CarbonFootprint_kg_Distribution ?CarbonFootprint_kg_Distribution;
            :CarbonFootprint_kg_EoL ?CarbonFootprint_kg_EoL;
            :CarbonFootprint_kg_Manufacturing ?CarbonFootprint_kg_Manufacturing;
            :CircularActivityCost ?CircularActivityCost;
            :DeviceCarbonFootprint ?DeviceCarbonFootprint;
            :DeviceCarbonFootprintErrorRatio ?DeviceCarbonFootprintErrorRatio;
            :EnergyConsumption ?EnergyConsumption;
            :EPDAvailability  ?EPDAvailability;
            :SourceHash ?SourceHash;
            :EPDSource ?EPDSource;
            :EPDDeviceLifetime ?EPDDeviceLifetime;
            :EPDDeviceWeight ?EPDDeviceWeight;
            :EPDUseLocation ?EPDUseLocation;
            :EPDFinalManufacturingLocation ?EPDFinalManufacturingLocation;
            :EPDUseEnergyDemand ?EPDUseEnergyDemand;
            :GHGCostProduction ?GHGCostProduction;
            :GHGCostUse ?GHGCostUse;
            :CarbonFootprintSource ?CarbonFootprintSource;
            :ProductSpecificationSource ?ProductSpecificationSource;
            :MaterialCompositionSource  ?MaterialCompositionSource;
            :MaterialRecyclability ?MaterialRecyclability;
            :AluminiumWeight ?AluminiumWeight;                   
            :CopperWeight ?CopperWeight;
            :SteelWeight ?SteelWeight;                                      
            :PlasticWeight ?PlasticWeight;
            :PCBWeight ?PCBWeight;
            :GlassesWeight ?GlassesWeight;
            :OtherMaterialsWeight ?OtherMaterialsWeight;
            :OtherMetalsWeight ?OtherMetalsWeight;
            :Waste ?Waste;
            :RecycledContent ?RecycledContent;
            
            :CollectionRateValue ?CollectionRateValue;
            :EoLRefurbishmentRate ?EoLRefurbishmentRate;
            :EoLRemanufacturingAluminium ?EoLRemanufacturingAluminium;                  
            :EoLRemanufacturingCopper ?EoLRemanufacturingCopper;                  
            :EoLRemanufacturingSteel ?EoLRemanufacturingSteel;                  
            :EoLRemanufacturingBattery ?EoLRemanufacturingBattery;                  
            :EoLRemanufacturingPCB ?EoLRemanufacturingPCB;                  
            :EoLRemanufacturingPlastic ?EoLRemanufacturingPlastic;                  
            :EoLRemanufacturingGlasses ?EoLRemanufacturingGlasses ;                  
            :EoLRemanufacturingOtherMaterials ?EoLRemanufacturingOtherMaterials;           
            :EoLRemanufacturingOtherMetals ?EoLRemanufacturingOtherMetals;
            
            :EoLRecycledCLAluminium ?EoLRecycledCLAluminium;
            :EoLRecycledCLCopper ?EoLRecycledCLCopper;
            :EoLRecycledCLSteel ?EoLRecycledCLSteel;
            :EoLRecycledCLBattery ?EoLRecycledCLBattery;
            :EoLRecycledCLGlasses ?EoLRecycledCLGlasses;
            :EoLRecycledCLPCB ?EoLRecycledCLPCB;
            :EoLRecycledCLPlastic ?EoLRecycledCLPlastic;
            :EoLRecycledCLOtherMetals ?EoLRecycledCLOtherMetals;
            :EoLRecycledCLOtherMaterials ?EoLRecycledCLOtherMaterials;
        
            :EoLRecycledOLAluminium ?EoLRecycledOLAluminium;
            :EoLRecycledOLCopper ?EoLRecycledOLCopper;
            :EoLRecycledOLSteel ?EoLRecycledOLSteel;
            :EoLRecycledOLBattery ?EoLRecycledOLBattery;
            :EoLRecycledOLGlasses ?EoLRecycledOLGlasses;
            :EoLRecycledOLPCB ?EoLRecycledOLPCB;
            :EoLRecycledOLPlastic ?EoLRecycledOLPlastic;
            :EoLRecycledOLOtherMetals ?EoLRecycledOLOtherMetals ;
            :EoLRecycledOLOtherMaterials ?EoLRecycledOLOtherMaterials.
    ?CircularStrategy :isSelectedCircularStrategyFor ?LaptopID;
                 :dueToReason ?Reason;
                 :startDate ?StartDate;
                 :endDate ?EndDate;
                 :hasStatus ?ProcessStatus.                                                     
    ?Agent :isResponsibleFor ?LaptopID;
          dpv:hasRole ?Role;
          :Email ?Email;
          :TelephoneNumber ?TelephoneNumber;
          :worksFor ?Company.
    FILTER(?LaptopID=:%s). 
    FILTER(?Status=:Refurbished). 
    }limit 1
    """ % (id)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    laptop_summary = {}
    # reformat some of the strings for better readability
    for laptop in results['results']['bindings']:
        laptop_id = id
        for var in vars:
            laptop_summary[var] = laptop[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        laptop_summary['id'] = laptop_id
    return laptop_summary

# /Agent/{id}
# Returns information about a specific agent.
@app.route('/Agent/<id>')
def get_agent(id):
    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
    PREFIX : <http://www.semanticweb.org/RePlanIT/>
    PREFIX dpv: <http://www.w3.org/ns/dpv#>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    select * where { 
        :%s a prov:Agent;
        :isResponsibleFor ?ICTDevice;
            dpv:hasRole ?Role;
            :Email ?Email;
            :TelephoneNumber ?TelephoneNumber;
            :worksFor ?Company.
        ?ICTDevice rdf:type ?Type;
                :hasBrand ?ICTDeviceBrand;
                :Model ?ICTDeviceModel.
        FILTER(?Type=:Laptop).
    } 
    """ % (id)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    agent_summary = []
    # reformat some of the strings for better readability
    for agent in results['results']['bindings']:
        agent_entry = {}
        for var in vars:
            agent_entry[var] = agent[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        agent_summary.append(agent_entry)
    return agent_summary

# /Units
# Return ionformation about measurement units
@app.route('/Units')
def get_units():
    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
    PREFIX : <http://www.semanticweb.org/RePlanIT/>
        select * where { 
        ?Indicator :hasMeasurementUnit ?Unit.   
    }
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    units_summary = []
    units_summary2 = {}
    # reformat some of the strings for better readability
    for unit in results['results']['bindings']:
        unit_entry = {}
        for var in vars:
            unit_entry[var] = unit[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        display_unit = unit['Unit']['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        if "blank_node" in display_unit:
            display_unit = "Unknown"
        units_summary2[unit['Indicator']['value'].replace('http://www.semanticweb.org/RePlanIT/', '')] =  display_unit
        units_summary.append(unit_entry)
    return units_summary2

# /LaptopCarbonFootprintManufacturingPerComponent/{id}
# Returns Laptop's carbon footprint during manufacturing per component
@app.route('/LaptopCarbonFootprintManufacturingPerComponent/<id>')
def get_laptop_carbon_foorprint(id):
    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
    PREFIX : <http://www.semanticweb.org/RePlanIT/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX obo: <http://purl.obolibrary.org/obo/>
    select * where{
        ?LaptopID rdf:type :Laptop.
        ?Component  :isComponentOf  ?LaptopID;
                    a ?Type;
                    :CarbonFootprintManufacturing ?CarbonFootprintManufacturingPerComponent.
            
        :CarbonFootprintManufacturing :hasMeasurementUnit ?Unit.
            
        FILTER(?LaptopID=:%s).
        FILTER(?Type=:Display ||?Type= :PCB||?Type= :Chassis
                ||?Type= :Packaging||?Type= :Cables||?Type=obo:NCIT_C49839
                ||?Type=:HardDrive||?Type=:OtherHardwareComponent).
    }
    """ % (id)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    footprint_summary = []
    # reformat some of the strings for better readability
    for component in results['results']['bindings']:
        component_entry = {}
        for var in vars:
            component_entry[var] = component[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        footprint_summary.append(component_entry)
    return footprint_summary

# verify the api token
def verify_token(token):
    auth_token = os.getenv('api_token')
    return token == auth_token

# verify the schema of the json body
def verify_schema(json_body, json_schema):
    for key in json_schema.keys():
        if not key in json_body:
            return False
    return True

# /InsertNewLaptopDPP
# Add a new laptop DPP to the knowledge graph
@app.route('/InsertNewLaptopDPP',  methods=["POST"])
def post_new_laptop():
    # check bearer token
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1] 
    # if the token is correct, then allow the query to execute
    if verify_token(token):
        # load the schema from json file
        schema_file = open('schema/new_laptop.json')
        json_schema = json.load(schema_file)
        # get the contents of the body
        json_body = request.get_json()
        # verify that the json body contains all the fields from the schema
        if verify_schema(json_body, json_schema):
            text_query = """
            PREFIX : <http://www.semanticweb.org/RePlanIT/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX unit: <https://qudt.org/2.1/vocab/unit/>
        PREFIX om-2:<http://www.ontology-of-units-of-measure.org/resource/om-2/>
        PREFIX dpv: <http://www.w3.org/ns/dpv#>
        PREFIX prov: <http://www.w3.org/ns/prov#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX obo: <http://purl.obolibrary.org/obo/>
        INSERT DATA{{
            :{ID} a :Laptop;
                    :AssemblyNumber "{AssemblyNumber}"^^xsd:string;
                    :hasBrand :{Brand};
                    :Model "{Model}"^^xsd:string;
                    :ModelYear "{ModelYear}"^^xsd:integer;
                    :hasStatus :{Status};
                    :DeliveryTime "{DeliveryTime}"^^xsd:double;
                    :ICTDeviceWeight "{ICTDeviceWeight}"^^xsd:double;
                    :hasCertification :EPEAT;
                    :hasCertification :SEPA;
                    :hasCertification :TCO;
                    :hasDeclarationType :EnvironmentalProductDeclaration;
                    :DeclarationDate "{DeclarationDate}"^^xsd:dateTime;
                    :PurchaseCostValue "{PurchaseCostValue}"^^xsd:double;
                    :CurrentCostValue "{CurrentCostValue}"^^xsd:double;                          
                    :MaintenanceCycles "{MaintenanceCycled}"^^xsd:double;
                    :hasSupport _:blankNode;
                    :SupportCostValue "{SupportCostValue}"^^xsd:double;
                    :hasOperatingSystem :{OperatingSystem};
                    :hasSecuritySoftware :{SecuritySoftware};
                    :WarrantyDuration "{WarrantyDuration}"^^xsd:double;
                    :Image "{Image}"^^xsd:anyURI;
                    :Temperature ""^^xsd:double;
                    :DisplayResolution "{DisplayResolution}"^^xsd:string;
                    :ScreenSize "{ScreenSize}"^^xsd:double;
                    :hasGraphicsCardProcessor :IntelIrisXGraphics;
                    :ClockRate "{ClockRate}"^^xsd:double;
                    :CameraPixels "{CameraPixels}"^^xsd:double;
                    :hasMemory :{Memory};
                    :hasComponent :SSD;
                    :RAMSize "{RAMSize}"^^xsd:integer;
                    :ROMSize "{ROMSize}"^^xsd:integer;
                    :BatteryCapacity "{BatteryCapacity}"^^xsd:double;
                    :BatteryLifetime "{BatteryLifetime}"^^xsd:double;
                    :BatteryWeight   "{BatteryWeight}"^^xsd:double;                      
                    :hasComponent :{CPU};
                    :hasCPUSeries :{CPUSeries};
                    :CPULoad ""^^xsd:double;
                    :CPUSpeed "{CPUSpeed}"^^xsd:double; 
                    :hasSensor :{Sensor};
                    :CarbonFootprintUse "{CarbonFootprintUse}"^^xsd:double;
                    :CarbonFootprintDistribution "{CarbonFootprintDistribution}"^^xsd:double;
                    :CarbonFootprintErrorratio "{CarbonFootprintErrorRatio}"^^xsd:double;
                    :CarbonFootprintEoL "{CarbonFootprintEoL}"^^xsd:double;
                    :CarbonFootprintManufacturing "{CarbonFootprintManufacturing}"^^xsd:double;
                    :CarbonFootprint_kg_Use "{CarbonFootprint_kg_Use}"^^xsd:double;
                    :CarbonFootprint_kg_Distribution "{CarbonFootprint_kg_Distribution}"^^xsd:double;
                    :CarbonFootprint_kg_EoL "{CarbonFootprint_kg_EoL}"^^xsd:double;
                    :CarbonFootprint_kg_Manufacturing "{CarbonFootprint_kg_Manufacturing}"^^xsd:double;
                    :CircularActivityCost "{CircularActivityCost}"^^xsd:double;
                    :DeviceCarbonFootprint "{DeviceCarbonFootprint}"^^xsd:double;
                    :DeviceCarbonFootprintErrorRatio "{DeviceCarbonFootprintErrorRatio}"^^xsd:double;
                    :EnergyConsumption "{EnergyConsumption}"^^xsd:double;
                    :EPDAvailability  "true"^^xsd:boolean;
                    :SourceHash "{SourceHash}"^^xsd:string;
                    :EPDSource "{EPDSource}"^^xsd:anyURI; 
                    :EPDDeviceLifetime "{EPDDeviceLifetime}"^^xsd:double;
                    :EPDDeviceWeight "{EPDDeviceWeight}"^^xsd:double;
                    :EPDUseLocation "{EPDUseLocation}"^^xsd:string;
                    :EPDFinalManufacturingLocation "{EPDFinalManufacturingLocation}"^^xsd:string;
                    :EPDUseEnergyDemand "{EPDUseEnergyDemand}"^^xsd:double;
                    :GHGCostProduction "{GHGCostProduction}"^^xsd:double;
                    :GHGCostUse "{GHGCostUse}"^^xsd:double;
                    :CarbonFootprintSource "{CarbonFootprintSource}"^^xsd:anyURI;
                    :ProductSpecificationSource "{ProductSpecificationSource}"^^xsd:anyURI;
                    :MaterialCompositionSource  "{MaterialCompositionSource}"^^xsd:anyURI;                            
                    :MaterialRecyclability ""^^xsd:boolean;
                    :AluminiumWeight "{AluminiumWeight}"^^xsd:double;                         
                    :CopperWeight "{CopperWeight}"^^xsd:double; 
                    :SteelWeight "{SteelWeight}"^^xsd:double;                                       
                    :PlasticWeight "{PlasticWeight}"^^xsd:double;
                    :PCBWeight "{PCBWeight}"^^xsd:double; 
                    :GlassesWeight "{GlassesWeight}"^^xsd:double; 
                    :OtherMaterialsWeight "{OtherMaterialsWeight}"^^xsd:double; 
                    :OtherMetalsWeight "{OtherMetalsWeight}"^^xsd:double;
                    :Waste "{Waste}"^^xsd:double;
                    :RecycledContent  "{RecycledContent}"^^xsd:integer;
                    :AluminiumRecycledContent ""^^xsd:double;
                    :BatteryRecycledContent ""^^xsd:double;
                    :CopperRecycledContent ""^^xsd:double;
                    :SteelRecycledContent ""^^xsd:double;                                                                                                       
                    :PCBRecycledContent ""^^xsd:double;
                    :GlassesRecycledContent ""^^xsd:double;
                    :OtherMetalsRecycledContent ""^^xsd:double;
                    :OtherMaterialsRecycledContent ""^^xsd:double;  
                    :CollectionRateValue "{CollectionRateValue}"^^xsd:double;
                    :EoLRefurbishmentRate "{EoLRefurbishmentRate}"^^xsd:double;
                    :EoLRemanufacturingAluminium "{EoLRemanufacturingAluminium}"^^xsd:double;                  
                    :EoLRemanufacturingCopper "{EoLRemanufacturingCopper}"^^xsd:double;                  
                    :EoLRemanufacturingSteel "{EoLRemanufacturingSteel}"^^xsd:double;                  
                    :EoLRemanufacturingBattery "{EoLRemanufacturingBattery}"^^xsd:double;                  
                    :EoLRemanufacturingPCB "{EoLRemanufacturingPCB}"^^xsd:double;                  
                    :EoLRemanufacturingPlastic "{EoLRemanufacturingPlastic}"^^xsd:double;                  
                    :EoLRemanufacturingGlasses "{EoLRemanufacturingGlasses}"^^xsd:double;                  
                    :EoLRemanufacturingOtherMaterials "{EoLRemanufacturingOtherMaterials}"^^xsd:double;                  
                    :EoLRemanufacturingOtherMetals "{EoLRemanufacturingOtherMetals}"^^xsd:double;
                    :EoLRecycledCLAluminium "{EoLRecycledCLAluminium}"^^xsd:double;
                    :EoLRecycledCLCopper "{EoLRecycledCLCopper}"^^xsd:double;
                    :EoLRecycledCLSteel "{EoLRecycledCLSteel}"^^xsd:double;
                    :EoLRecycledCLBattery "{EoLRecycledCLBattery}"^^xsd:double;
                    :EoLRecycledCLGlasses "{EoLRecycledCLGlasses}"^^xsd:double;
                    :EoLRecycledCLPCB "{EoLRecycledCLPCB}"^^xsd:double;
                    :EoLRecycledCLPlastic "{EoLRecycledCLPlastic}"^^xsd:double;
                    :EoLRecycledCLOtherMetals "{EoLRecycledCLOtherMetals}"^^xsd:double;
                    :EoLRecycledCLOtherMaterials "{EoLRecycledCLOtherMaterials}"^^xsd:double;                        
                    :EoLRecycledOLAluminium "{EoLRecycledOLAluminium}"^^xsd:double;
                    :EoLRecycledOLCopper "{EoLRecycledOLCopper}"^^xsd:double;
                    :EoLRecycledOLSteel "{EoLRecycledOLSteel}"^^xsd:double;
                    :EoLRecycledOLBattery "{EoLRecycledOLBattery}"^^xsd:double;
                    :EoLRecycledOLGlasses "{EoLRecycledOLGlasses}"^^xsd:double;
                    :EoLRecycledOLPCB "{EoLRecycledOLPCB}"^^xsd:double;
                    :EoLRecycledOLPlastic "{EoLRecycledOLPlastic}"^^xsd:double;
                    :EoLRecycledOLOtherMetals "{EoLRecycledOLOtherMetals}"^^xsd:double;
                    :EoLRecycledOLOtherMaterials "{EoLRecycledOLOtherMaterials}"^^xsd:double.


            :{AgentID} a prov:Agent;
                    a prov:Organization;
                    dpv:hasRole :{AgentRole};
                    :Email "{AgentEmail}"^^xsd:string;
                    :TelephoneNumber "{AgentTelephoneNumber}"^^xsd:string;
                    :worksFor :{AgentCompany};
                    :isResponsibleFor :{ID}.
            
            
            :09df74ca-7863-430b-95d7-256bf6ex7aca a :HardwareComponent;
                    a :Display;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "15.80"^^xsd:double.
            
            :05df74aa-7863-4c0b-95d7-a56fd6ef3ax3 a :HardwareComponent;
                    a :PCB;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "39.10"^^xsd:double.
            
            :09fs73aa-7863-4c0b-95d7-25abd6ef73cx a :HardwareComponent;
                    a :Cables;  
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "2.10"^^xsd:double.
            
            :0f5f74aa-7863-4afb-95d7-256bsfef7cax a :HardwareComponent; 
                    a :Chassis;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "6.40"^^xsd:double.
            
            :502f74aa-7863-4fab-95d7-356bdcescxbb a :HardwareComponent;
                    a obo:NCIT_C49839;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "3.20"^^xsd:double.

            :092f7aaa-fx63-4s0b-95d7-256bd6efc43b a :HardwareComponent;
                    a :HardDrive;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "31.30"^^xsd:double.

            :042fc4fa-7x63-4axb-95d7-256bd6es73bc a :HardwareComponent;
                    a :Packaging;
                    :isPackagingFor :{ID};
                    :CarbonFootprintManufacturing "0.30"^^xsd:double.

            :03xf74aa-7363-4s0b-95d7-256ss6effakc a :HardwareComponent;
                    a :OtherHardwareComponent;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "1.70"^^xsd:double.  
            
            :{ID} :hasIndicator :PurchaseCost;
                    :hasIndicator :CurrentCost;
                    :hasIndicator :TrueCost;
                    :hasIndicator :CircularActivityCost;
                    :hasIndicator :DeliveryTime;
                    :hasIndicator :ICTDeviceWeight;
                    :hasIndicator :MaterialWeight;
                    :hasIndicator :ClockRate;
                    :hasIndicator :CameraPixels;
                    :hasIndicator :CPULoad;
                    :hasIndicator :CPUSpeed;
                    :hasIndicator :BatteryCapacity;
                    :hasIndicator :BatteryLifetime;
                    :hasIndicator :BatteryWeight;
                    :hasIndicator :Memory;
                    :hasIndicator :ScreenSize;
                    :hasIndicator :GreenHouseGasCost;
                    :hasIndicator :GreenHouseGasCostProduction;
                    :hasIndicator :CarbonFootprintUse;
                    :hasIndicator :CarbonFootprintDistribution;
                    :hasIndicator :CarbonFootprintEoL;
                    :hasIndicator :CarbonFootprintErrorRatio;
                    :hasIndicator :CarbonFootprintManufacturing;
                    :hasIndicator :WarrantyDuration;
                    :hasIndicator :EnergyConsumption;
                    :hasIndicator :GreenHouseGasEmissions;
                    :hasIndicator :MaterialCircularity;
                    :hasIndicator :UseEnergyDemand;
                    :hasIndicator :Waste;
                    :hasIndicator :CollectionRate;
                    :hasIndicator :EoLRecycledCL;
                    :hasIndicator :EoLRecycledOL;
                    :hasIndicator :EoLRemanufacturing.
                    }}   
            """
            sparql = SPARQLWrapper(graphdb_url + "/statements")
            sparql.setCredentials(user=username, passwd=password)
            real_query = text_query.format(**json_body)
            sparql.setQuery(real_query)
            sparql.method = 'POST'
            sparql.query()
            return "Created", 201
        else:
            return "Invalid Schema", 400
    else:
        return "Invalid bearer token", 401
    
# /InsertRefurbishedLaptopDPPPP
# Add a refurbished laptop DPP to the knowledge graph
@app.route('/InsertRefurbishedLaptopDPP',  methods=["POST"])
def post_refurbished_laptop():
    # check bearer token
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    # if the token is correct, then allow the query to execute
    if verify_token(token):
        # load the schema from json file
        schema_file = open('schema/new_laptop.json')
        json_schema = json.load(schema_file)
        # get the contents of the body
        json_body = request.get_json()
        json_body['CircularStrategyReason'] = json_body['CircularStrategyReason'].replace(" ", "")
        json_body['Sensor'] = json_body['Sensor'].replace(" ", "")
        # verify that the json body contains all the fields from the schema
        if verify_schema(json_body, json_schema):
            text_query = """
            PREFIX : <http://www.semanticweb.org/RePlanIT/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX unit: <https://qudt.org/2.1/vocab/unit/>
            PREFIX om-2:<http://www.ontology-of-units-of-measure.org/resource/om-2/>
            PREFIX dpv: <http://www.w3.org/ns/dpv#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX obo: <http://purl.obolibrary.org/obo/>
            INSERT DATA{{
            :{ID} a :Laptop;
                    :AssemblyNumber "{AssemblyNumber}"^^xsd:string;
                    :hasBrand :{Brand};
                    :Model "{Model}"^^xsd:string;
                    :ModelYear "{ModelYear}"^^xsd:integer;
                    :hasStatus :{Status};
                    :DeliveryTime "{DeliveryTime}"^^xsd:double;
                    :ICTDeviceWeight "{ICTDeviceWeight}"^^xsd:double;
                    :hasCertification :EPEAT;
                    :hasCertification :SEPA;
                    :hasCertification :TCO;
                    :hasDeclarationType :EnvironmentalProductDeclaration;
                    :DeclarationDate "{DeclarationDate}"^^xsd:dateTime;
                    :PurchaseCostValue "{PurchaseCostValue}"^^xsd:double;
                    :CurrentCostValue "{CurrentCostValue}"^^xsd:double;                          
                    :MaintenanceCycles "{MaintenanceCycled}"^^xsd:double;
                    :hasSupport _:blankNode;
                    :SupportCostValue "{SupportCostValue}"^^xsd:double;
                    :hasOperatingSystem :{OperatingSystem};
                    :hasSecuritySoftware :{SecuritySoftware};
                    :WarrantyDuration "{WarrantyDuration}"^^xsd:double;
                    :Image "{Image}"^^xsd:anyURI;
                    :Temperature ""^^xsd:double;
                    :DisplayResolution "{DisplayResolution}"^^xsd:string;
                    :ScreenSize "{ScreenSize}"^^xsd:double;
                    :hasGraphicsCardProcessor :IntelIrisXGraphics;
                    :ClockRate "{ClockRate}"^^xsd:double;
                    :CameraPixels "{CameraPixels}"^^xsd:double;
                    :hasMemory :{Memory};
                    :hasComponent :SSD;
                    :RAMSize "{RAMSize}"^^xsd:integer;
                    :ROMSize "{ROMSize}"^^xsd:integer;
                    :BatteryCapacity "{BatteryCapacity}"^^xsd:double;
                    :BatteryLifetime "{BatteryLifetime}"^^xsd:double;
                    :BatteryWeight   "{BatteryWeight}"^^xsd:double;                      
                    :hasComponent :{CPU};
                    :hasCPUSeries :{CPUSeries};
                    :CPULoad ""^^xsd:double;
                    :CPUSpeed "{CPUSpeed}"^^xsd:double; 
                    :hasSensor :{Sensor};
                    :CarbonFootprintUse "{CarbonFootprintUse}"^^xsd:double;
                    :CarbonFootprintDistribution "{CarbonFootprintDistribution}"^^xsd:double;
                    :CarbonFootprintErrorratio "{CarbonFootprintErrorRatio}"^^xsd:double;
                    :CarbonFootprintEoL "{CarbonFootprintEoL}"^^xsd:double;
                    :CarbonFootprintManufacturing "{CarbonFootprintManufacturing}"^^xsd:double;
                    :CarbonFootprint_kg_Use "{CarbonFootprint_kg_Use}"^^xsd:double;
                    :CarbonFootprint_kg_Distribution "{CarbonFootprint_kg_Distribution}"^^xsd:double;
                    :CarbonFootprint_kg_EoL "{CarbonFootprint_kg_EoL}"^^xsd:double;
                    :CarbonFootprint_kg_Manufacturing "{CarbonFootprint_kg_Manufacturing}"^^xsd:double;
                    :CircularActivityCost "{CircularActivityCost}"^^xsd:double;
                    :DeviceCarbonFootprint "{DeviceCarbonFootprint}"^^xsd:double;
                    :DeviceCarbonFootprintErrorRatio "{DeviceCarbonFootprintErrorRatio}"^^xsd:double;
                    :EnergyConsumption "{EnergyConsumption}"^^xsd:double;
                    :EPDAvailability  "true"^^xsd:boolean;
                    :SourceHash "{SourceHash}"^^xsd:string;
                    :EPDSource "{EPDSource}"^^xsd:anyURI; 
                    :EPDDeviceLifetime "{EPDDeviceLifetime}"^^xsd:double;
                    :EPDDeviceWeight "{EPDDeviceWeight}"^^xsd:double;
                    :EPDUseLocation "{EPDUseLocation}"^^xsd:string;
                    :EPDFinalManufacturingLocation "{EPDFinalManufacturingLocation}"^^xsd:string;
                    :EPDUseEnergyDemand "{EPDUseEnergyDemand}"^^xsd:double;
                    :GHGCostProduction "{GHGCostProduction}"^^xsd:double;
                    :GHGCostUse "{GHGCostUse}"^^xsd:double;
                    :CarbonFootprintSource "{CarbonFootprintSource}"^^xsd:anyURI;
                    :ProductSpecificationSource "{ProductSpecificationSource}"^^xsd:anyURI;
                    :MaterialCompositionSource  "{MaterialCompositionSource}"^^xsd:anyURI;                            
                    :MaterialRecyclability ""^^xsd:boolean;
                    :AluminiumWeight "{AluminiumWeight}"^^xsd:double;                         
                    :CopperWeight "{CopperWeight}"^^xsd:double; 
                    :SteelWeight "{SteelWeight}"^^xsd:double;                                       
                    :PlasticWeight "{PlasticWeight}"^^xsd:double;
                    :PCBWeight "{PCBWeight}"^^xsd:double; 
                    :GlassesWeight "{GlassesWeight}"^^xsd:double; 
                    :OtherMaterialsWeight "{OtherMaterialsWeight}"^^xsd:double; 
                    :OtherMetalsWeight "{OtherMetalsWeight}"^^xsd:double;
                    :Waste "{Waste}"^^xsd:double;
                    :RecycledContent  "{RecycledContent}"^^xsd:integer;
                    :AluminiumRecycledContent ""^^xsd:double;
                    :BatteryRecycledContent ""^^xsd:double;
                    :CopperRecycledContent ""^^xsd:double;
                    :SteelRecycledContent ""^^xsd:double;                                                                                                       
                    :PCBRecycledContent ""^^xsd:double;
                    :GlassesRecycledContent ""^^xsd:double;
                    :OtherMetalsRecycledContent ""^^xsd:double;
                    :OtherMaterialsRecycledContent ""^^xsd:double;  
                    :CollectionRateValue "{CollectionRateValue}"^^xsd:double;
                    :EoLRefurbishmentRate "{EoLRefurbishmentRate}"^^xsd:double;
                    :EoLRemanufacturingAluminium "{EoLRemanufacturingAluminium}"^^xsd:double;                  
                    :EoLRemanufacturingCopper "{EoLRemanufacturingCopper}"^^xsd:double;                  
                    :EoLRemanufacturingSteel "{EoLRemanufacturingSteel}"^^xsd:double;                  
                    :EoLRemanufacturingBattery "{EoLRemanufacturingBattery}"^^xsd:double;                  
                    :EoLRemanufacturingPCB "{EoLRemanufacturingPCB}"^^xsd:double;                  
                    :EoLRemanufacturingPlastic "{EoLRemanufacturingPlastic}"^^xsd:double;                  
                    :EoLRemanufacturingGlasses "{EoLRemanufacturingGlasses}"^^xsd:double;                  
                    :EoLRemanufacturingOtherMaterials "{EoLRemanufacturingOtherMaterials}"^^xsd:double;                  
                    :EoLRemanufacturingOtherMetals "{EoLRemanufacturingOtherMetals}"^^xsd:double;
                    :EoLRecycledCLAluminium "{EoLRecycledCLAluminium}"^^xsd:double;
                    :EoLRecycledCLCopper "{EoLRecycledCLCopper}"^^xsd:double;
                    :EoLRecycledCLSteel "{EoLRecycledCLSteel}"^^xsd:double;
                    :EoLRecycledCLBattery "{EoLRecycledCLBattery}"^^xsd:double;
                    :EoLRecycledCLGlasses "{EoLRecycledCLGlasses}"^^xsd:double;
                    :EoLRecycledCLPCB "{EoLRecycledCLPCB}"^^xsd:double;
                    :EoLRecycledCLPlastic "{EoLRecycledCLPlastic}"^^xsd:double;
                    :EoLRecycledCLOtherMetals "{EoLRecycledCLOtherMetals}"^^xsd:double;
                    :EoLRecycledCLOtherMaterials "{EoLRecycledCLOtherMaterials}"^^xsd:double;                        
                    :EoLRecycledOLAluminium "{EoLRecycledOLAluminium}"^^xsd:double;
                    :EoLRecycledOLCopper "{EoLRecycledOLCopper}"^^xsd:double;
                    :EoLRecycledOLSteel "{EoLRecycledOLSteel}"^^xsd:double;
                    :EoLRecycledOLBattery "{EoLRecycledOLBattery}"^^xsd:double;
                    :EoLRecycledOLGlasses "{EoLRecycledOLGlasses}"^^xsd:double;
                    :EoLRecycledOLPCB "{EoLRecycledOLPCB}"^^xsd:double;
                    :EoLRecycledOLPlastic "{EoLRecycledOLPlastic}"^^xsd:double;
                    :EoLRecycledOLOtherMetals "{EoLRecycledOLOtherMetals}"^^xsd:double;
                    :EoLRecycledOLOtherMaterials "{EoLRecycledOLOtherMaterials}"^^xsd:double.

                :Refurbishment :isSelectedCircularStrategyFor :{ID};
                        :dueToReason :{CircularStrategyReason};
                        :startDate "{CircularStrategyStartDate}"^^xsd:dateTime;
                        :endDate "{CircularStrategyEndDate}"^^xsd:dateTime;
                        :hasStatus :{CircularStrategyStatus}.

            :{AgentID} a prov:Agent;
                    a prov:Organization;
                    dpv:hasRole :{AgentRole};
                    :Email "{AgentEmail}"^^xsd:string;
                    :TelephoneNumber "{AgentTelephoneNumber}"^^xsd:string;
                    :worksFor :{AgentCompany};
                    :isResponsibleFor :{ID}.
            
            
            :09df74ca-7863-430b-95d7-256bf6ex7aca a :HardwareComponent;
                    a :Display;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "15.80"^^xsd:double.
            
            :05df74aa-7863-4c0b-95d7-a56fd6ef3ax3 a :HardwareComponent;
                    a :PCB;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "39.10"^^xsd:double.
            
            :09fs73aa-7863-4c0b-95d7-25abd6ef73cx a :HardwareComponent;
                    a :Cables;  
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "2.10"^^xsd:double.
            
            :0f5f74aa-7863-4afb-95d7-256bsfef7cax a :HardwareComponent; 
                    a :Chassis;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "6.40"^^xsd:double.
            
            :502f74aa-7863-4fab-95d7-356bdcescxbb a :HardwareComponent;
                    a obo:NCIT_C49839;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "3.20"^^xsd:double.

            :092f7aaa-fx63-4s0b-95d7-256bd6efc43b a :HardwareComponent;
                    a :HardDrive;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "31.30"^^xsd:double.

            :042fc4fa-7x63-4axb-95d7-256bd6es73bc a :HardwareComponent;
                    a :Packaging;
                    :isPackagingFor :{ID};
                    :CarbonFootprintManufacturing "0.30"^^xsd:double.

            :03xf74aa-7363-4s0b-95d7-256ss6effakc a :HardwareComponent;
                    a :OtherHardwareComponent;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "1.70"^^xsd:double.  
            
            :{ID} :hasIndicator :PurchaseCost;
                    :hasIndicator :CurrentCost;
                    :hasIndicator :TrueCost;
                    :hasIndicator :CircularActivityCost;
                    :hasIndicator :DeliveryTime;
                    :hasIndicator :ICTDeviceWeight;
                    :hasIndicator :MaterialWeight;
                    :hasIndicator :ClockRate;
                    :hasIndicator :CameraPixels;
                    :hasIndicator :CPULoad;
                    :hasIndicator :CPUSpeed;
                    :hasIndicator :BatteryCapacity;
                    :hasIndicator :BatteryLifetime;
                    :hasIndicator :BatteryWeight;
                    :hasIndicator :Memory;
                    :hasIndicator :ScreenSize;
                    :hasIndicator :GreenHouseGasCost;
                    :hasIndicator :GreenHouseGasCostProduction;
                    :hasIndicator :CarbonFootprintUse;
                    :hasIndicator :CarbonFootprintDistribution;
                    :hasIndicator :CarbonFootprintEoL;
                    :hasIndicator :CarbonFootprintErrorRatio;
                    :hasIndicator :CarbonFootprintManufacturing;
                    :hasIndicator :WarrantyDuration;
                    :hasIndicator :EnergyConsumption;
                    :hasIndicator :GreenHouseGasEmissions;
                    :hasIndicator :MaterialCircularity;
                    :hasIndicator :UseEnergyDemand;
                    :hasIndicator :Waste;
                    :hasIndicator :CollectionRate;
                    :hasIndicator :EoLRecycledCL;
                    :hasIndicator :EoLRecycledOL;
                    :hasIndicator :EoLRemanufacturing.
            }} 
            """
            sparql = SPARQLWrapper(graphdb_url + "/statements")
            sparql.setCredentials(user=username, passwd=password)
            real_query = text_query.format(**json_body)
            sparql.setQuery(real_query)
            sparql.method = 'POST'
            sparql.query()
            return "Created", 201
        else:
            return "Invalid Schema", 400
    else:
        return "Invalid bearer token", 401

# /InsertRepairedLaptopDPP
# Add a repaired laptop DPP to the knowledge graph
@app.route('/InsertRepairedLaptopDPP',  methods=["POST"])
def post_repaired_laptop():
    # check bearer token
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    # if the token is correct, then allow the query to execute
    if verify_token(token):
        # load the schema from json file
        schema_file = open('schema/new_laptop.json')
        json_schema = json.load(schema_file)
        # get the contents of the body
        json_body = request.get_json()
        json_body['CircularStrategyReason'] = json_body['CircularStrategyReason'].replace(" ", "")
        json_body['Sensor'] = json_body['Sensor'].replace(" ", "")
        # verify that the json body contains all the fields from the schema
        if verify_schema(json_body, json_schema):
            text_query = """
            PREFIX : <http://www.semanticweb.org/RePlanIT/>
            PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
            PREFIX unit: <https://qudt.org/2.1/vocab/unit/>
            PREFIX om-2:<http://www.ontology-of-units-of-measure.org/resource/om-2/>
            PREFIX dpv: <http://www.w3.org/ns/dpv#>
            PREFIX prov: <http://www.w3.org/ns/prov#>
            PREFIX owl: <http://www.w3.org/2002/07/owl#>
            PREFIX obo: <http://purl.obolibrary.org/obo/>
            INSERT DATA{{
            :{ID} a :Laptop;
                    :AssemblyNumber "{AssemblyNumber}"^^xsd:string;
                    :hasBrand :{Brand};
                    :Model "{Model}"^^xsd:string;
                    :ModelYear "{ModelYear}"^^xsd:integer;
                    :hasStatus :{Status};
                    :DeliveryTime "{DeliveryTime}"^^xsd:double;
                    :ICTDeviceWeight "{ICTDeviceWeight}"^^xsd:double;
                    :hasCertification :EPEAT;
                    :hasCertification :SEPA;
                    :hasCertification :TCO;
                    :hasDeclarationType :EnvironmentalProductDeclaration;
                    :DeclarationDate "{DeclarationDate}"^^xsd:dateTime;
                    :PurchaseCostValue "{PurchaseCostValue}"^^xsd:double;
                    :CurrentCostValue "{CurrentCostValue}"^^xsd:double;                          
                    :MaintenanceCycles "{MaintenanceCycled}"^^xsd:double;
                    :hasSupport _:blankNode;
                    :SupportCostValue "{SupportCostValue}"^^xsd:double;
                    :hasOperatingSystem :{OperatingSystem};
                    :hasSecuritySoftware :{SecuritySoftware};
                    :WarrantyDuration "{WarrantyDuration}"^^xsd:double;
                    :Image "{Image}"^^xsd:anyURI;
                    :Temperature ""^^xsd:double;
                    :DisplayResolution "{DisplayResolution}"^^xsd:string;
                    :ScreenSize "{ScreenSize}"^^xsd:double;
                    :hasGraphicsCardProcessor :IntelIrisXGraphics;
                    :ClockRate "{ClockRate}"^^xsd:double;
                    :CameraPixels "{CameraPixels}"^^xsd:double;
                    :hasMemory :{Memory};
                    :hasComponent :SSD;
                    :RAMSize "{RAMSize}"^^xsd:integer;
                    :ROMSize "{ROMSize}"^^xsd:integer;
                    :BatteryCapacity "{BatteryCapacity}"^^xsd:double;
                    :BatteryLifetime "{BatteryLifetime}"^^xsd:double;
                    :BatteryWeight   "{BatteryWeight}"^^xsd:double;                      
                    :hasComponent :{CPU};
                    :hasCPUSeries :{CPUSeries};
                    :CPULoad ""^^xsd:double;
                    :CPUSpeed "{CPUSpeed}"^^xsd:double; 
                    :hasSensor :{Sensor};
                    :CarbonFootprintUse "{CarbonFootprintUse}"^^xsd:double;
                    :CarbonFootprintDistribution "{CarbonFootprintDistribution}"^^xsd:double;
                    :CarbonFootprintErrorratio "{CarbonFootprintErrorRatio}"^^xsd:double;
                    :CarbonFootprintEoL "{CarbonFootprintEoL}"^^xsd:double;
                    :CarbonFootprintManufacturing "{CarbonFootprintManufacturing}"^^xsd:double;
                    :CarbonFootprint_kg_Use "{CarbonFootprint_kg_Use}"^^xsd:double;
                    :CarbonFootprint_kg_Distribution "{CarbonFootprint_kg_Distribution}"^^xsd:double;
                    :CarbonFootprint_kg_EoL "{CarbonFootprint_kg_EoL}"^^xsd:double;
                    :CarbonFootprint_kg_Manufacturing "{CarbonFootprint_kg_Manufacturing}"^^xsd:double;
                    :CircularActivityCost "{CircularActivityCost}"^^xsd:double;
                    :DeviceCarbonFootprint "{DeviceCarbonFootprint}"^^xsd:double;
                    :DeviceCarbonFootprintErrorRatio "{DeviceCarbonFootprintErrorRatio}"^^xsd:double;
                    :EnergyConsumption "{EnergyConsumption}"^^xsd:double;
                    :EPDAvailability  "true"^^xsd:boolean;
                    :SourceHash "{SourceHash}"^^xsd:string;
                    :EPDSource "{EPDSource}"^^xsd:anyURI; 
                    :EPDDeviceLifetime "{EPDDeviceLifetime}"^^xsd:double;
                    :EPDDeviceWeight "{EPDDeviceWeight}"^^xsd:double;
                    :EPDUseLocation "{EPDUseLocation}"^^xsd:string;
                    :EPDFinalManufacturingLocation "{EPDFinalManufacturingLocation}"^^xsd:string;
                    :EPDUseEnergyDemand "{EPDUseEnergyDemand}"^^xsd:double;
                    :GHGCostProduction "{GHGCostProduction}"^^xsd:double;
                    :GHGCostUse "{GHGCostUse}"^^xsd:double;
                    :CarbonFootprintSource "{CarbonFootprintSource}"^^xsd:anyURI;
                    :ProductSpecificationSource "{ProductSpecificationSource}"^^xsd:anyURI;
                    :MaterialCompositionSource  "{MaterialCompositionSource}"^^xsd:anyURI;                            
                    :MaterialRecyclability ""^^xsd:boolean;
                    :AluminiumWeight "{AluminiumWeight}"^^xsd:double;                         
                    :CopperWeight "{CopperWeight}"^^xsd:double; 
                    :SteelWeight "{SteelWeight}"^^xsd:double;                                       
                    :PlasticWeight "{PlasticWeight}"^^xsd:double;
                    :PCBWeight "{PCBWeight}"^^xsd:double; 
                    :GlassesWeight "{GlassesWeight}"^^xsd:double; 
                    :OtherMaterialsWeight "{OtherMaterialsWeight}"^^xsd:double; 
                    :OtherMetalsWeight "{OtherMetalsWeight}"^^xsd:double;
                    :Waste "{Waste}"^^xsd:double;
                    :RecycledContent  "{RecycledContent}"^^xsd:integer;
                    :AluminiumRecycledContent ""^^xsd:double;
                    :BatteryRecycledContent ""^^xsd:double;
                    :CopperRecycledContent ""^^xsd:double;
                    :SteelRecycledContent ""^^xsd:double;                                                                                                       
                    :PCBRecycledContent ""^^xsd:double;
                    :GlassesRecycledContent ""^^xsd:double;
                    :OtherMetalsRecycledContent ""^^xsd:double;
                    :OtherMaterialsRecycledContent ""^^xsd:double;  
                    :CollectionRateValue "{CollectionRateValue}"^^xsd:double;
                    :EoLRefurbishmentRate "{EoLRefurbishmentRate}"^^xsd:double;
                    :EoLRemanufacturingAluminium "{EoLRemanufacturingAluminium}"^^xsd:double;                  
                    :EoLRemanufacturingCopper "{EoLRemanufacturingCopper}"^^xsd:double;                  
                    :EoLRemanufacturingSteel "{EoLRemanufacturingSteel}"^^xsd:double;                  
                    :EoLRemanufacturingBattery "{EoLRemanufacturingBattery}"^^xsd:double;                  
                    :EoLRemanufacturingPCB "{EoLRemanufacturingPCB}"^^xsd:double;                  
                    :EoLRemanufacturingPlastic "{EoLRemanufacturingPlastic}"^^xsd:double;                  
                    :EoLRemanufacturingGlasses "{EoLRemanufacturingGlasses}"^^xsd:double;                  
                    :EoLRemanufacturingOtherMaterials "{EoLRemanufacturingOtherMaterials}"^^xsd:double;                  
                    :EoLRemanufacturingOtherMetals "{EoLRemanufacturingOtherMetals}"^^xsd:double;
                    :EoLRecycledCLAluminium "{EoLRecycledCLAluminium}"^^xsd:double;
                    :EoLRecycledCLCopper "{EoLRecycledCLCopper}"^^xsd:double;
                    :EoLRecycledCLSteel "{EoLRecycledCLSteel}"^^xsd:double;
                    :EoLRecycledCLBattery "{EoLRecycledCLBattery}"^^xsd:double;
                    :EoLRecycledCLGlasses "{EoLRecycledCLGlasses}"^^xsd:double;
                    :EoLRecycledCLPCB "{EoLRecycledCLPCB}"^^xsd:double;
                    :EoLRecycledCLPlastic "{EoLRecycledCLPlastic}"^^xsd:double;
                    :EoLRecycledCLOtherMetals "{EoLRecycledCLOtherMetals}"^^xsd:double;
                    :EoLRecycledCLOtherMaterials "{EoLRecycledCLOtherMaterials}"^^xsd:double;                        
                    :EoLRecycledOLAluminium "{EoLRecycledOLAluminium}"^^xsd:double;
                    :EoLRecycledOLCopper "{EoLRecycledOLCopper}"^^xsd:double;
                    :EoLRecycledOLSteel "{EoLRecycledOLSteel}"^^xsd:double;
                    :EoLRecycledOLBattery "{EoLRecycledOLBattery}"^^xsd:double;
                    :EoLRecycledOLGlasses "{EoLRecycledOLGlasses}"^^xsd:double;
                    :EoLRecycledOLPCB "{EoLRecycledOLPCB}"^^xsd:double;
                    :EoLRecycledOLPlastic "{EoLRecycledOLPlastic}"^^xsd:double;
                    :EoLRecycledOLOtherMetals "{EoLRecycledOLOtherMetals}"^^xsd:double;
                    :EoLRecycledOLOtherMaterials "{EoLRecycledOLOtherMaterials}"^^xsd:double.

                :Refurbishment :isSelectedCircularStrategyFor :{ID};
                        :dueToReason :{CircularStrategyReason};
                        :startDate "{CircularStrategyStartDate}"^^xsd:dateTime;
                        :endDate "{CircularStrategyEndDate}"^^xsd:dateTime;
                        :hasStatus :{CircularStrategyStatus}.

            :{AgentID} a prov:Agent;
                    a prov:Organization;
                    dpv:hasRole :{AgentRole};
                    :Email "{AgentEmail}"^^xsd:string;
                    :TelephoneNumber "{AgentTelephoneNumber}"^^xsd:string;
                    :worksFor :{AgentCompany};
                    :isResponsibleFor :{ID}.
            
            
            :09df74ca-7863-430b-95d7-256bf6ex7aca a :HardwareComponent;
                    a :Display;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "15.80"^^xsd:double.
            
            :05df74aa-7863-4c0b-95d7-a56fd6ef3ax3 a :HardwareComponent;
                    a :PCB;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "39.10"^^xsd:double.
            
            :09fs73aa-7863-4c0b-95d7-25abd6ef73cx a :HardwareComponent;
                    a :Cables;  
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "2.10"^^xsd:double.
            
            :0f5f74aa-7863-4afb-95d7-256bsfef7cax a :HardwareComponent; 
                    a :Chassis;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "6.40"^^xsd:double.
            
            :502f74aa-7863-4fab-95d7-356bdcescxbb a :HardwareComponent;
                    a obo:NCIT_C49839;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "3.20"^^xsd:double.

            :092f7aaa-fx63-4s0b-95d7-256bd6efc43b a :HardwareComponent;
                    a :HardDrive;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "31.30"^^xsd:double.

            :042fc4fa-7x63-4axb-95d7-256bd6es73bc a :HardwareComponent;
                    a :Packaging;
                    :isPackagingFor :{ID};
                    :CarbonFootprintManufacturing "0.30"^^xsd:double.

            :03xf74aa-7363-4s0b-95d7-256ss6effakc a :HardwareComponent;
                    a :OtherHardwareComponent;
                    :isComponentOf :{ID};
                    :CarbonFootprintManufacturing "1.70"^^xsd:double.  
            
            :{ID} :hasIndicator :PurchaseCost;
                    :hasIndicator :CurrentCost;
                    :hasIndicator :TrueCost;
                    :hasIndicator :CircularActivityCost;
                    :hasIndicator :DeliveryTime;
                    :hasIndicator :ICTDeviceWeight;
                    :hasIndicator :MaterialWeight;
                    :hasIndicator :ClockRate;
                    :hasIndicator :CameraPixels;
                    :hasIndicator :CPULoad;
                    :hasIndicator :CPUSpeed;
                    :hasIndicator :BatteryCapacity;
                    :hasIndicator :BatteryLifetime;
                    :hasIndicator :BatteryWeight;
                    :hasIndicator :Memory;
                    :hasIndicator :ScreenSize;
                    :hasIndicator :GreenHouseGasCost;
                    :hasIndicator :GreenHouseGasCostProduction;
                    :hasIndicator :CarbonFootprintUse;
                    :hasIndicator :CarbonFootprintDistribution;
                    :hasIndicator :CarbonFootprintEoL;
                    :hasIndicator :CarbonFootprintErrorRatio;
                    :hasIndicator :CarbonFootprintManufacturing;
                    :hasIndicator :WarrantyDuration;
                    :hasIndicator :EnergyConsumption;
                    :hasIndicator :GreenHouseGasEmissions;
                    :hasIndicator :MaterialCircularity;
                    :hasIndicator :UseEnergyDemand;
                    :hasIndicator :Waste;
                    :hasIndicator :CollectionRate;
                    :hasIndicator :EoLRecycledCL;
                    :hasIndicator :EoLRecycledOL;
                    :hasIndicator :EoLRemanufacturing.
            }} 
            """
            sparql = SPARQLWrapper(graphdb_url + "/statements")
            sparql.setCredentials(user=username, passwd=password)
            real_query = text_query.format(**json_body)
            sparql.setQuery(real_query)
            sparql.method = 'POST'
            sparql.query()
            return "Created", 201
        else:
            return "Invalid Schema", 400
    else:
        return "Invalid bearer token", 401
    
# /DPPPurchaseCost/{id}
# Update the purchase cost of a device
@app.route('/DPPPurchaseCost/<id>',  methods=["PUT"])
def put_purchase_cost_laptop(id):
    headers = request.headers
    bearer = headers.get('Authorization')
    token = bearer.split()[1]
    # if the token is correct, then allow the query to execute
    if verify_token(token):
        # get the contents of the body
        json_body = float(request.get_json())
        # verify that the json body contains all the fields from the schema
        text_query = """
        PREFIX : <http://www.semanticweb.org/RePlanIT/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>


        Delete {?ICTDevice :PurchaseCostValue ?x}
        Insert {?ICTDevice :PurchaseCostValue "%s"^^xsd:double}
        Where
        {?ICTDevice a :Laptop.
            ?ICTDevice :PurchaseCostValue ?x.
            FILTER(?ICTDevice=:%s).
        } 
        """ % (json_body, id)
        sparql = SPARQLWrapper(graphdb_url + "/statements")
        sparql.setCredentials(user=username, passwd=password)
        sparql.setQuery(text_query)
        sparql.method = 'POST'
        sparql.query()
        return "Created", 201
    else:
        return "Invalid bearer token", 401
    
# /NewDataServerDPP
# Returns a new data server's DPP
@app.route('/NewDataServerDPP/<id>')
def get_newdataserverdpp(id):
    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
    PREFIX : <http://www.semanticweb.org/RePlanIT/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX unit: <https://qudt.org/2.1/vocab/>
    PREFIX om-2: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    PREFIX dpv: <http://www.w3.org/ns/dpv#>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    select * where { 
    ?DataServerID a :DataServer;
    :AssemblyNumber ?AssemblyNumber;
    :hasBrand ?Brand;
    :Model ?Model;
    :ModelYear ?ModelYear;
    :hasStatus ?Status;
    :DeliveryTime ?DeliveryTime;
    :ICTDeviceWeight ?Weight;
    :hasDeclarationType ?Declaration;
    :DeclarationDate ?DeclarationDate;
    :PurchaseCostValue ?PurchaseCost;
    :CurrentCostValue ?CurrentCost;                          
    :MaintenanceCycles ?MaintenanceCycles;
    :hasSupport ?Support;
    :TrueCostValue ?TrueCostValue;
    :SupportCostValue ?SupportCostValue;
    :hasSoftware ?hasSoftware;
    :hasOperatingSystem ?hasOperatingSystem;
    :WarrantyDuration ?WarrantyDuration;
    :WarrantyDetails  ?WarrantyDetails;                 
    :Temperature ?Temperature;
    :ClockRate ?ClockRate;
    :NVDIMMRank ?NVDIMMRank;
    :NVDIMMCapacity ?NVDIMMCapacity;
    :MemorySlots ?MemorySlots; 
    :CPUSpeed   ?CPUSpeed;                 
    :MinCPUCache ?MinCPUCache; 
    :MaxCPUCache ?MaxCPUCache;
    :ServerGeneration ?ServerGeneration;          
    :CPULoad ?CPULoad;
    :hasMemory ?hasMemory; 
    :ExpansionSlotNumber ?ExpansionSlotNumber;
    :CarbonFootprintUse ?CarbonFootprintUse;
    :CarbonFootprintDistribution ?CarbonFootprintDistribution;
    :CarbonFootprintErrorratio ?CarbonFootprintErrorratio;
    :CarbonFootprintEoL ?CarbonFootprintEoL;
    :CarbonFootprintManufacturing ?CarbonFootprintManufacturing;
    :CarbonFootprint_kg_Use ?CarbonFootprint_kg_Use;
    :CarbonFootprint_kg_Distribution ?CarbonFootprint_kg_Distribution;
    :CarbonFootprint_kg_EoL ?CarbonFootprint_kg_EoL;
    :CarbonFootprint_kg_Manufacturing ?CarbonFootprint_kg_Manufacturing;
    :CircularActivityCost ?CircularActivityCost;
    :DeviceCarbonFootprint ?DeviceCarbonFootprint;
    :DeviceCarbonFootprintErrorRatio ?DeviceCarbonFootprintErrorRatio;
    :EnergyConsumption ?EnergyConsumption;
    :EPDAvailability  ?EPDAvailability;
    :SourceHash ?SourceHash;
    :EPDSource ?EPDSource; 
    :EPDDeviceLifetime ?EPDDeviceLifetime;
    :EPDDeviceWeight ?EPDDeviceWeight;
    :EPDUseLocation ?EPDUseLocation;
    :EPDFinalManufacturingLocation ?EPDFinalManufacturingLocation;
    :EPDUseEnergyDemand ?EPDUseEnergyDemand;
    :GHGCostProduction ?GHGCostProduction;
    :GHGCostUse ?GHGCostUse;
    :CarbonFootprintSource ?CarbonFootprintSource;
    :MaterialCompositionSource  ?MaterialCompositionSource;                            
    :MaterialRecyclability ?MaterialRecyclability;

    :AluminiumWeight ?AluminiumWeight;                         
    :CopperWeight ?CopperWeight; 
    :SteelWeight ?SteelWeight;                                       
    :PlasticWeight ?PlasticWeight;
    :PCBWeight ?PCBWeight; 
    :GlassesWeight ?GlassesWeight; 
    :OtherMaterialsWeight ?OtherMaterialsWeight; 
    :OtherMetalsWeight ?OtherMetalsWeight;
    :Waste ?Waste;
    :RecycledContent  ?RecycledContent;
    :AluminiumRecycledContent ?AluminiumRecycledContent;
    :BatteryRecycledContent ?BatteryRecycledContent;
    :CopperRecycledContent ?CopperRecycledContent;
    :SteelRecycledContent ?SteelRecycledContent;
    :PCBRecycledContent ?PCBRecycledContent;
    :GlassesRecycledContent ?GlassesRecycledContent;
    :OtherMetalsRecycledContent ?OtherMetalsRecycledContent;
    :OtherMaterialsRecycledContent ?OtherMaterialsRecycledContent;

    :CollectionRateValue ?CollectionRateValue;
    :EoLRefurbishmentRate ?EoLRefurbishmentRate;

    :EoLRemanufacturingAluminium ?EoLRemanufacturingAluminium;                  
    :EoLRemanufacturingCopper ?EoLRemanufacturingCopper;                  
    :EoLRemanufacturingSteel ?EoLRemanufacturingSteel;                  
    :EoLRemanufacturingBattery ?EoLRemanufacturingBattery;                  
    :EoLRemanufacturingPCB ?EoLRemanufacturingPCB;                  
    :EoLRemanufacturingPlastic ?EoLRemanufacturingPlastic;                  
    :EoLRemanufacturingGlasses ?EoLRemanufacturingGlasses;                  
    :EoLRemanufacturingOtherMaterials ?EoLRemanufacturingOtherMaterials;                  
    :EoLRemanufacturingOtherMetals ?EoLRemanufacturingOtherMetals;

    :EoLRecycledCLAluminium ?EoLRecycledCLAluminium;
    :EoLRecycledCLCopper ?EoLRecycledCLCopper;
    :EoLRecycledCLSteel ?EoLRecycledCLSteel;
    :EoLRecycledCLBattery ?EoLRecycledCLBattery;
    :EoLRecycledCLGlasses ?EoLRecycledCLGlasses;
    :EoLRecycledCLPCB ?EoLRecycledCLPCB;
    :EoLRecycledCLPlastic ?EoLRecycledCLPlastic;
    :EoLRecycledCLOtherMetals ?EoLRecycledCLOtherMetals;
    :EoLRecycledCLOtherMaterials ?EoLRecycledCLOtherMaterials;

    :EoLRecycledOLAluminium ?EoLRecycledOLAluminium;
    :EoLRecycledOLCopper ?EoLRecycledOLCopper;
    :EoLRecycledOLSteel ?EoLRecycledOLSteel;
    :EoLRecycledOLBattery ?EoLRecycledOLBattery;
    :EoLRecycledOLGlasses ?EoLRecycledOLGlasses;
    :EoLRecycledOLPCB ?EoLRecycledOLPCB;
    :EoLRecycledOLPlastic ?EoLRecycledOLPlastic;
    :EoLRecycledOLOtherMetals ?EoLRecycledOLOtherMetals;
    :EoLRecycledOLOtherMaterials ?EoLRecycledOLOtherMaterials.
        
    ?Agent :isResponsibleFor ?LaptopID;
            dpv:hasRole ?AgentRole;
            :Email ?AgentEmail;
            :TelephoneNumber ?AgentTelephoneNumber;
            :worksFor ?AgentCompany.

    FILTER(?DataServerID=:%s).
    FILTER(?Status=:New). 
    }
    """ % (id)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    laptop_summary = {}
    # reformat some of the strings for better readability
    for laptop in results['results']['bindings']:
        laptop_id = id
        for var in vars:
            laptop_summary[var] = laptop[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        laptop_summary['id'] = laptop_id
    laptop_summary['hasCertification'] = get_collection("DataServer", "hasCertification", id, "New")
    laptop_summary['hasSecuritySoftware'] = get_collection("DataServer", "hasSecuritySoftware", id, "New")
    laptop_summary['Image'] = get_collection("DataServer", "Image", id, "New")
    laptop_summary['hasComponent'] = get_collection("DataServer", "hasComponent", id, "New")
    return laptop_summary

# Get a collection from a specific field of a device
def get_collection(device_type, field, id, status):
    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
    PREFIX : <http://www.semanticweb.org/RePlanIT/>
    select * where { 
        ?%sID a :%s;
            :hasStatus ?Status;
            :%s ?%s.
    FILTER(?DataServerID=:%s). 
    FILTER(?Status=:%s). 
    }
    """ % (device_type, device_type, field, field, id, status)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    collection  = []
    # reformat some of the strings for better readability
    for laptop in results['results']['bindings']:
        collection.append(laptop[field]['value'].replace('http://www.semanticweb.org/RePlanIT/', ''))
    return collection

# /RefurbishedDataServerDPP
# Returns a refurbished data server's DPP
@app.route('/RefurbishedDataServerDPP/<id>')
def get_refurbisheddataserverdpp(id):
    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
    PREFIX : <http://www.semanticweb.org/RePlanIT/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX unit: <https://qudt.org/2.1/vocab/>
    PREFIX om-2: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    PREFIX dpv: <http://www.w3.org/ns/dpv#>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    select * where { 
    ?DataServerID a :DataServer;
    :AssemblyNumber ?AssemblyNumber;
    :hasBrand ?Brand;
    :Model ?Model;
    :ModelYear ?ModelYear;
    :hasStatus ?Status;
    :DeliveryTime ?DeliveryTime;
    :ICTDeviceWeight ?Weight;
    :hasDeclarationType ?Declaration;
    :DeclarationDate ?DeclarationDate;
    :PurchaseCostValue ?PurchaseCost;
    :CurrentCostValue ?CurrentCost;                          
    :MaintenanceCycles ?MaintenanceCycles;
    :hasSupport ?Support;
    :TrueCostValue ?TrueCostValue;
    :SupportCostValue ?SupportCostValue;
    :hasSoftware ?hasSoftware;
    :hasOperatingSystem ?hasOperatingSystem;
    :WarrantyDuration ?WarrantyDuration;
    :WarrantyDetails  ?WarrantyDetails;                 
    :Temperature ?Temperature;
    :ClockRate ?ClockRate;
    :NVDIMMRank ?NVDIMMRank;
    :NVDIMMCapacity ?NVDIMMCapacity;
    :MemorySlots ?MemorySlots; 
    :CPUSpeed   ?CPUSpeed;                 
    :MinCPUCache ?MinCPUCache; 
    :MaxCPUCache ?MaxCPUCache;
    :ServerGeneration ?ServerGeneration;          
    :CPULoad ?CPULoad;
    :hasMemory ?hasMemory; 
    :ExpansionSlotNumber ?ExpansionSlotNumber;
    :CarbonFootprintUse ?CarbonFootprintUse;
    :CarbonFootprintDistribution ?CarbonFootprintDistribution;
    :CarbonFootprintErrorratio ?CarbonFootprintErrorratio;
    :CarbonFootprintEoL ?CarbonFootprintEoL;
    :CarbonFootprintManufacturing ?CarbonFootprintManufacturing;
    :CarbonFootprint_kg_Use ?CarbonFootprint_kg_Use;
    :CarbonFootprint_kg_Distribution ?CarbonFootprint_kg_Distribution;
    :CarbonFootprint_kg_EoL ?CarbonFootprint_kg_EoL;
    :CarbonFootprint_kg_Manufacturing ?CarbonFootprint_kg_Manufacturing;
    :CircularActivityCost ?CircularActivityCost;
    :DeviceCarbonFootprint ?DeviceCarbonFootprint;
    :DeviceCarbonFootprintErrorRatio ?DeviceCarbonFootprintErrorRatio;
    :EnergyConsumption ?EnergyConsumption;
    :EPDAvailability  ?EPDAvailability;
    :SourceHash ?SourceHash;
    :EPDSource ?EPDSource; 
    :EPDDeviceLifetime ?EPDDeviceLifetime;
    :EPDDeviceWeight ?EPDDeviceWeight;
    :EPDUseLocation ?EPDUseLocation;
    :EPDFinalManufacturingLocation ?EPDFinalManufacturingLocation;
    :EPDUseEnergyDemand ?EPDUseEnergyDemand;
    :GHGCostProduction ?GHGCostProduction;
    :GHGCostUse ?GHGCostUse;
    :CarbonFootprintSource ?CarbonFootprintSource;
    :MaterialCompositionSource  ?MaterialCompositionSource;                            
    :MaterialRecyclability ?MaterialRecyclability;

    :AluminiumWeight ?AluminiumWeight;                         
    :CopperWeight ?CopperWeight; 
    :SteelWeight ?SteelWeight;                                       
    :PlasticWeight ?PlasticWeight;
    :PCBWeight ?PCBWeight; 
    :GlassesWeight ?GlassesWeight; 
    :OtherMaterialsWeight ?OtherMaterialsWeight; 
    :OtherMetalsWeight ?OtherMetalsWeight;
    :Waste ?Waste;
    :RecycledContent  ?RecycledContent;
    :AluminiumRecycledContent ?AluminiumRecycledContent;
    :BatteryRecycledContent ?BatteryRecycledContent;
    :CopperRecycledContent ?CopperRecycledContent;
    :SteelRecycledContent ?SteelRecycledContent;
    :PCBRecycledContent ?PCBRecycledContent;
    :GlassesRecycledContent ?GlassesRecycledContent;
    :OtherMetalsRecycledContent ?OtherMetalsRecycledContent;
    :OtherMaterialsRecycledContent ?OtherMaterialsRecycledContent;

    :CollectionRateValue ?CollectionRateValue;
    :EoLRefurbishmentRate ?EoLRefurbishmentRate;

    :EoLRemanufacturingAluminium ?EoLRemanufacturingAluminium;                  
    :EoLRemanufacturingCopper ?EoLRemanufacturingCopper;                  
    :EoLRemanufacturingSteel ?EoLRemanufacturingSteel;                  
    :EoLRemanufacturingBattery ?EoLRemanufacturingBattery;                  
    :EoLRemanufacturingPCB ?EoLRemanufacturingPCB;                  
    :EoLRemanufacturingPlastic ?EoLRemanufacturingPlastic;                  
    :EoLRemanufacturingGlasses ?EoLRemanufacturingGlasses;                  
    :EoLRemanufacturingOtherMaterials ?EoLRemanufacturingOtherMaterials;                  
    :EoLRemanufacturingOtherMetals ?EoLRemanufacturingOtherMetals;

    :EoLRecycledCLAluminium ?EoLRecycledCLAluminium;
    :EoLRecycledCLCopper ?EoLRecycledCLCopper;
    :EoLRecycledCLSteel ?EoLRecycledCLSteel;
    :EoLRecycledCLBattery ?EoLRecycledCLBattery;
    :EoLRecycledCLGlasses ?EoLRecycledCLGlasses;
    :EoLRecycledCLPCB ?EoLRecycledCLPCB;
    :EoLRecycledCLPlastic ?EoLRecycledCLPlastic;
    :EoLRecycledCLOtherMetals ?EoLRecycledCLOtherMetals;
    :EoLRecycledCLOtherMaterials ?EoLRecycledCLOtherMaterials;

    :EoLRecycledOLAluminium ?EoLRecycledOLAluminium;
    :EoLRecycledOLCopper ?EoLRecycledOLCopper;
    :EoLRecycledOLSteel ?EoLRecycledOLSteel;
    :EoLRecycledOLBattery ?EoLRecycledOLBattery;
    :EoLRecycledOLGlasses ?EoLRecycledOLGlasses;
    :EoLRecycledOLPCB ?EoLRecycledOLPCB;
    :EoLRecycledOLPlastic ?EoLRecycledOLPlastic;
    :EoLRecycledOLOtherMetals ?EoLRecycledOLOtherMetals;
    :EoLRecycledOLOtherMaterials ?EoLRecycledOLOtherMaterials.
        
    ?Agent :isResponsibleFor ?LaptopID;
            dpv:hasRole ?AgentRole;
            :Email ?AgentEmail;
            :TelephoneNumber ?AgentTelephoneNumber;
            :worksFor ?AgentCompany.

    FILTER(?DataServerID=:%s).
    FILTER(?Status=:Refurbished). 
    }
    """ % (id)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    laptop_summary = {}
    # reformat some of the strings for better readability
    for laptop in results['results']['bindings']:
        laptop_id = id
        for var in vars:
            laptop_summary[var] = laptop[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        laptop_summary['id'] = laptop_id
    laptop_summary['hasCertification'] = get_collection("DataServer", "hasCertification", id, "Refurbished")
    laptop_summary['hasSecuritySoftware'] = get_collection("DataServer", "hasSecuritySoftware", id, "Refurbished")
    laptop_summary['Image'] = get_collection("DataServer", "Image", id, "Refurbished")
    laptop_summary['hasComponent'] = get_collection("DataServer", "hasComponent", id, "Refurbished")
    return laptop_summary


# /AllDataServerDPPs
# Returns all data server's DPP
@app.route('/AllDataServerDPPs')
def get_alldataserverdpp():
        # get the limit variable if it is present in the URL parameters
    # and prepare the string for the query
    limit = request.args.get('limit')
    limit_string = ""
    if limit is None:
        limit_string = ""
    else:
        limit_string = "limit %s" % (limit)

    # connect to graphdb and execute the query
    sparql = SPARQLWrapper(graphdb_url)
    sparql.setCredentials(user=username, passwd=password)
    query = """
    PREFIX : <http://www.semanticweb.org/RePlanIT/>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX unit: <https://qudt.org/2.1/vocab/>
    PREFIX om-2: <http://www.ontology-of-units-of-measure.org/resource/om-2/>
    PREFIX dpv: <http://www.w3.org/ns/dpv#>
    PREFIX prov: <http://www.w3.org/ns/prov#>
    select * where { 
    ?DataServerID a :DataServer;
        :AssemblyNumber ?AssemblyNumber;
        :hasBrand ?Brand;
        :Model ?Model;
        :ModelYear ?ModelYear;
        :hasStatus ?Status;
    } %s
    """ % (limit_string)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    vars = results['head']['vars']
    laptop_summary = {}
    dataservers = []
    # reformat some of the strings for better readability
    for laptop in results['results']['bindings']:
        laptop_summary = {}
        for var in vars:
            laptop_summary[var] = laptop[var]['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        laptop_summary['id'] = laptop['DataServerID']['value'].replace('http://www.semanticweb.org/RePlanIT/', '')
        dataservers.append(laptop_summary)
    return dataservers
    

if __name__ == '__main__':
    app.run()
