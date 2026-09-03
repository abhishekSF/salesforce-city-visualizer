import json

# Write metadataCatalog.js
metadata_catalog_code = '''export const METADATA_CATALOG = {
  districts: {
    metadata: {
      id: 'metadata',
      name: 'Metadata Citadel',
      subtitle: 'Schema, SObjects & Security Perimeter',
      badgeColor: '#3b82f6',
      icon: '🏢',
      description: 'The declarative backbone of Salesforce. Defines standard and custom schema objects, relationships, fields, validation logic, and the security trust perimeter (Profiles, Permission Sets, FLS, and OWD).'
    },
    automation: {
      id: 'automation',
      name: 'Logic & Automation Grid',
      subtitle: 'Apex, Flows & Event-Driven Engine',
      badgeColor: '#eab308',
      icon: '⚡',
      description: 'The execution powerhouse. Orchestrates business rules through transactional Apex (WITH USER_MODE), asynchronous queues, autolaunched Flows, and high-throughput Platform Events.'
    },
    semantic: {
      id: 'semantic',
      name: 'Data Cloud & Semantic Harbor',
      subtitle: 'DLOs, DMOs, Identity Resolution & Vectors',
      badgeColor: '#06b6d4',
      icon: '🌊',
      description: 'The semantic context layer. Ingests poly-cloud data into Data Lake Objects (DLOs), harmonizes them into Data Model Objects (DMOs), unifies identities into a Golden Record, computes Calculated Insights, and indexes unstructured assets into Vector RAG.'
    },
    headless: {
      id: 'headless',
      name: 'Headless 360 Skyport',
      subtitle: 'Decoupled HXL, GraphQL & Composable APIs',
      badgeColor: '#10b981',
      icon: '🚀',
      description: 'The API is the UI. Decouples the Customer 360 from browser DOMs (LEX), powering headless experiences across Slack, mobile consoles, custom React frontends, and external client agents with microsecond latency.'
    },
    agentforce: {
      id: 'agentforce',
      name: 'Agentforce Autonomous Hub',
      subtitle: 'Atlas Reasoning Engine, Topics & Guardrails',
      badgeColor: '#8b5cf6',
      icon: '🤖',
      description: 'Salesforce autonomous AI agent headquarters. Powered by the Atlas Reasoning Engine, orchestrating autonomous SDR and service coworkers (like Kaveri) grounded in Data Cloud and governed by the Einstein Trust Layer.'
    },
    claudeforce: {
      id: 'claudeforce',
      name: 'Claudeforce Research Complex',
      subtitle: 'Anthropic Claude 3.5 Multi-Modal Co-Intelligence',
      badgeColor: '#f97316',
      icon: '🧠',
      description: 'Advanced cognitive observatory fusing Anthropic Claude 3.5 Sonnet and Haiku with Salesforce. Excels at multi-modal document reasoning (invoices, manifests, PDFs), deep Apex code synthesis, and natural language SOQL.'
    },
    mcp: {
      id: 'mcp',
      name: 'MCP & API Interchange',
      subtitle: 'Dual-Plane MCP Servers & Modern Protocols',
      badgeColor: '#ec4899',
      icon: '🔌',
      description: 'The universal AI-CRM connective tissue. Implements the Dual-Plane Model Context Protocol (Plane 1 Data 360 for Context, Plane 2 Headless 360 for Action), along with GraphQL, Tooling, Composite, and Pub/Sub gRPC APIs.'
    }
  },

  buildings: [
    {
      id: 'b_standard_objects',
      districtId: 'metadata',
      name: 'Standard Objects Tower',
      type: 'skyscraper',
      subtitle: 'Account, Contact, Opportunity, Case, Lead',
      floors: 64,
      gridX: 4,
      gridY: 4,
      width: 2,
      height: 2,
      color: '#3b82f6',
      roofType: 'antenna',
      relationships: ['b_custom_objects', 'b_security_fortress', 'b_flow_powerhouse'],
      tags: ['SObject', 'Schema', 'Core CRM', 'Relational'],
      summary: 'The bedrock relational entities powering CRM data structures, standard relationship graphs, and transactional auditing.',
      metrics: { records: '1.4M', fields: 420, relationships: 18, apiVersions: 'v66.0' },
      schemaSnippet: `<!-- Account.object-meta.xml -->
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <enableFeeds>true</enableFeeds>
    <enableHistory>true</enableHistory>
    <sharingModel>Private</sharingModel>
    <fields>
        <fullName>Industry_Vertical__c</fullName>
        <type>Picklist</type>
        <valueSet>
            <valueSetDefinition>
                <value><fullName>ColdChain_Logistics</fullName><default>true</default></value>
                <value><fullName>Biotech_LifeSciences</fullName><default>false</default></value>
                <value><fullName>Depot_Energy</fullName><default>false</default></value>
            </valueSetDefinition>
        </valueSet>
    </fields>
</CustomObject>`,
      explanation: 'Standard Objects form the core domain models of Salesforce CRM. Each object is fully auditable with Field History Tracking, System Modstamp, and deterministic relationships (Lookups and Master-Detail).'
    },
    {
      id: 'b_custom_objects',
      districtId: 'metadata',
      name: 'Custom Objects Works (__c)',
      type: 'factory',
      subtitle: 'INDRA_Shipment__c, Depot_Asset__c, Sensor_Reading__c',
      floors: 32,
      gridX: 2,
      gridY: 7,
      width: 2,
      height: 2,
      color: '#2563eb',
      roofType: 'smokestack',
      relationships: ['b_standard_objects', 'b_data_lake', 'b_apex_foundry'],
      tags: ['Custom SObject', 'Schema', 'Foreign Keys', '__c'],
      summary: 'Custom schema factory tailoring Salesforce to specific enterprise domains like freight linehauls, cold-chain telemetry, and EV chargers.',
      metrics: { customObjects: 48, customFields: 680, junctionObjects: 6 },
      schemaSnippet: `// SOQL Query for Custom Object Relationship Graph
SELECT Id, Name, INDRA_Consignee__r.Name, 
       INDRA_Origin_Depot__r.Depot_Code__c,
       INDRA_Temp_Excursion_Flag__c,
       (SELECT Id, StageName, Amount FROM Opportunities__r)
FROM INDRA_Shipment__c
WHERE INDRA_Status__c = 'In_Transit'
  AND INDRA_Priority__c = 'Critical_Medical'`,
      explanation: 'Custom Objects (__c) extend Salesforce with bespoke tables, rollup summary fields, formula fields, and Master-Detail cascades that enforce referential integrity across business units.'
    },
    {
      id: 'b_security_fortress',
      districtId: 'metadata',
      name: 'Security & Governance Citadel',
      type: 'fortress',
      subtitle: 'Profiles, Permission Sets, FLS & OWD Moat',
      floors: 40,
      gridX: 6,
      gridY: 2,
      width: 2,
      height: 2,
      color: '#1d4ed8',
      roofType: 'dome',
      relationships: ['b_standard_objects', 'b_headless_gateway', 'b_mcp_headless'],
      tags: ['Security', 'FLS', 'OWD', 'PermSets', 'Shield'],
      summary: 'Enforces the enterprise trust perimeter. Field-Level Security (FLS), Row-Level Sharing, and Session-based Permission Sets guarantee zero unauthorized data leakage.',
      metrics: { permSets: 84, sharingRules: 32, owdStrictness: 'High (Private)', shieldActive: true },
      schemaSnippet: `<!-- Harbor_Care_Concierge.permissionset-meta.xml -->
<PermissionSet xmlns="http://soap.sforce.com/2006/04/metadata">
    <hasActivationRequired>false</hasActivationRequired>
    <label>Harbor Care Concierge Specialist</label>
    <fieldPermissions>
        <editable>true</editable>
        <field>INDRA_Shipment__c.Temp_Excursion_Flag__c</field>
        <readable>true</readable>
    </fieldPermissions>
    <objectPermissions>
        <allowCreate>true</allowCreate>
        <allowDelete>false</allowDelete>
        <allowEdit>true</allowEdit>
        <allowRead>true</allowRead>
        <object>INDRA_Shipment__c</object>
    </objectPermissions>
</PermissionSet>`,
      explanation: 'Salesforce security applies multi-layered enforcement: Org-Wide Defaults (OWD) establish the baseline privacy, Role Hierarchies open vertical access, Sharing Rules provide lateral access, and Permission Sets control FLS and CRUD per field.'
    },
    {
      id: 'b_flow_powerhouse',
      districtId: 'automation',
      name: 'Flow Hydro-Automation Plant',
      type: 'substation',
      subtitle: 'Record-Triggered, Screen & Orchestrator Flows',
      floors: 28,
      gridX: 11,
      gridY: 3,
      width: 2,
      height: 2,
      color: '#eab308',
      roofType: 'solar',
      relationships: ['b_apex_foundry', 'b_events_hub', 'b_agentforce_core'],
      tags: ['Flow', 'Declarative Logic', 'Orchestration', 'Async'],
      summary: 'Visual declarative execution engine processing millions of transactions per day, with sub-flow modularity and deterministic rollback capabilities.',
      metrics: { activeFlows: 112, orchestrations: 8, avgExecTime: '34ms' },
      schemaSnippet: `<!-- Flow Definition (Snippet) -->
<Flow xmlns="http://soap.sforce.com/2006/04/metadata">
    <apiVersion>66.0</apiVersion>
    <processType>AutoLaunchedFlow</processType>
    <start>
        <object>INDRA_Shipment__c</object>
        <recordTriggerType>Update</recordTriggerType>
        <triggerType>RecordAfterSave</triggerType>
        <filters>
            <field>Temp_Excursion_Flag__c</field>
            <operator>EqualTo</operator>
            <value><booleanValue>true</booleanValue></value>
        </filters>
    </start>
    <actionCalls>
        <name>Trigger_Harbor_Care_Rescue</name>
        <actionName>INDRA_UnifiedContextService</actionName>
        <actionType>apex</actionType>
    </actionCalls>
</Flow>`,
      explanation: 'Flows provide declarative visual automation. Record-Triggered Flows run Before-Save (for high-speed field updates) and After-Save (for cross-object logic and publishing Platform Events).'
    },
    {
      id: 'b_apex_foundry',
      districtId: 'automation',
      name: 'Apex Foundry & Queueables',
      type: 'foundry',
      subtitle: 'Service Layer (WITH USER_MODE), Batch & Triggers',
      floors: 50,
      gridX: 14,
      gridY: 5,
      width: 2,
      height: 2,
      color: '#ca8a04',
      roofType: 'antenna',
      relationships: ['b_flow_powerhouse', 'b_mcp_headless', 'b_claudeforce_lab'],
      tags: ['Apex', 'OOP', 'WITH USER_MODE', 'Batchable', 'Queueable'],
      summary: 'The strongly-typed Java-like execution engine running in multi-tenant isolation, enforcing governor limits, heap boundaries, and secure query modes.',
      metrics: { codeCoverage: '94%', classes: 320, triggers: 12, queueableDepth: 5 },
      schemaSnippet: `public with sharing class INDRA_UnifiedContextService {
    @InvocableMethod(label='Dispatch Cold-Chain Rescue' category='Agentforce')
    public static List<RescueResult> executeRescue(List<RescueRequest> requests) {
        List<RescueResult> results = new List<RescueResult>();
        for (RescueRequest req : requests) {
            // Enforce compile-time user mode security
            INDRA_Care_Case__c careCase = new INDRA_Care_Case__c(
                Shipment__c = req.shipmentId,
                Severity__c = 'Critical_P0',
                Protocol__c = 'GHMC_Monsoon_Rescue'
            );
            insert as user careCase;
            
            // Fire event for real-time Headless 360 notification
            EventBus.publish(new INDRA_Care_Signal__e(
                Case_Id__c = careCase.Id,
                Household_Id__c = req.householdId
            ));
            results.add(new RescueResult(careCase.Id, true));
        }
        return results;
    }
}`,
      explanation: 'Apex code powers complex backend enterprise logic. Modern best practices enforce "WITH USER_MODE" and "as user" syntax to automatically respect Field-Level Security and Sharing Rules without manual checks.'
    },
    {
      id: 'b_events_hub',
      districtId: 'automation',
      name: 'Platform Event Bus & CDC Relay',
      type: 'transmitter',
      subtitle: 'High-Volume Events, Change Data Capture & Pub/Sub',
      floors: 36,
      gridX: 9,
      gridY: 7,
      width: 2,
      height: 2,
      color: '#a16207',
      roofType: 'radar',
      relationships: ['b_flow_powerhouse', 'b_headless_gateway', 'b_mcp_headless'],
      tags: ['Platform Events', 'CDC', 'Event-Driven', 'Kafka Backbone', 'gRPC'],
      summary: 'The event-driven messaging backbone built on Apache Kafka, broadcasting state changes to external subscribers with 72-hour replay retention.',
      metrics: { eventsPerDay: '8.4M', latency: '12ms', retentionHours: 72 },
      schemaSnippet: `<!-- INDRA_Care_Signal__e.object-meta.xml -->
<CustomObject xmlns="http://soap.sforce.com/2006/04/metadata">
    <deploymentStatus>Deployed</deploymentStatus>
    <eventType>HighVolume</eventType>
    <label>INDRA Care Signal</label>
    <fields>
        <fullName>Household_Id__c</fullName>
        <type>Text</type>
        <length>50</length>
    </fields>
    <fields>
        <fullName>Payload_JSON__c</fullName>
        <type>LongTextArea</type>
        <length>131072</length>
    </fields>
</CustomObject>`,
      explanation: 'Platform Events decouple producers and consumers. External microservices subscribe via the modern Pub/Sub API over gRPC, streaming delta events without polling.'
    },
    {
      id: 'b_data_lake',
      districtId: 'semantic',
      name: 'Data Lake Reservoirs (DLOs)',
      type: 'lake_docks',
      subtitle: 'Raw Streaming & Batch Ingestion from Poly-Clouds',
      floors: 24,
      gridX: 19,
      gridY: 3,
      width: 3,
      height: 2,
      color: '#06b6d4',
      roofType: 'water_basin',
      relationships: ['b_harmonizer', 'b_calculated_insights', 'b_mcp_context'],
      tags: ['Data Cloud', 'DLO', 'Zero-Copy', 'Lakehouse', 'BigQuery'],
      summary: 'Ingests petabyte-scale telemetry, Snowflake/BigQuery Zero-Copy shares, IoT telematics, and web clickstreams into raw immutable Data Lake Objects.',
      metrics: { ingestedGB: '480 TB', streams: 14, zeroCopyShares: 4 },
      schemaSnippet: `// Data Lake Object (DLO) Schema Mapping
{
  "dlo_name": "DLO_Shipment_Telemetry__dll",
  "source": "Kafka_Fleet_Telemetry_Topic",
  "fields": [
    { "name": "Telemetry_UUID", "type": "Text", "pk": true },
    { "name": "Depot_ID", "type": "Text" },
    { "name": "Temp_Celsius", "type": "Number" },
    { "name": "Grid_Load_kW", "type": "Number" },
    { "name": "Ingestion_Timestamp", "type": "DateTime" }
  ]
}`,
      explanation: 'Data Lake Objects (DLOs) preserve raw data as ingested from external sources without mutation, supporting real-time streaming ingestion and Zero-Copy data virtualization from Snowflake or Google BigQuery.'
    },
    {
      id: 'b_harmonizer',
      districtId: 'semantic',
      name: 'Identity Resolution & DMO Refinery',
      type: 'refinery',
      subtitle: 'Unified Individual Graph, Golden Record & Standard DMOs',
      floors: 45,
      gridX: 21,
      gridY: 7,
      width: 2,
      height: 2,
      color: '#0891b2',
      roofType: 'pipes',
      relationships: ['b_data_lake', 'b_vector_vault', 'b_mcp_context'],
      tags: ['Semantic Layer', 'DMO', 'Identity Resolution', 'Golden Record', 'Graph'],
      summary: 'Harmonizes raw DLOs into the CIM (Cloud Information Model) Standard DMOs and runs probabilistic & deterministic rules to unify fragmented customer identities into a single Golden Record.',
      metrics: { matchRate: '96.2%', unifiedIndividuals: '420K', rulesActive: 5 },
      schemaSnippet: `// Identity Resolution Rule Spec
{
  "ruleset": "Unified_Individual_Ruleset",
  "match_rules": [
    {
      "type": "Deterministic",
      "fields": ["NormalizedPhone_E164", "NormalizedEmail"]
    },
    {
      "type": "Probabilistic",
      "fields": ["FuzzyName_JaroWinkler_0.85", "ExactPostalCode"]
    }
  ],
  "survivorship": {
    "Name": "MostFrequentlyOccurring",
    "ContactPoints": "PreserveAllActiveVerified"
  }
}`,
      explanation: 'Identity Resolution bridges the gap between B2B and B2C identities. A single individual (e.g. Dr. Meera Reddy) across an enterprise CRM contact, an e-commerce consignee, and a clinic account is unified into a single Unified Individual UID.'
    },
    {
      id: 'b_vector_vault',
      districtId: 'semantic',
      name: 'Vector & Embedding RAG Vault',
      type: 'vault',
      subtitle: 'Semantic Search, Hybrid RAG & Knowledge Embeddings',
      floors: 38,
      gridX: 18,
      gridY: 8,
      width: 2,
      height: 2,
      color: '#0e7490',
      roofType: 'crystal',
      relationships: ['b_harmonizer', 'b_agentforce_core', 'b_claudeforce_lab'],
      tags: ['Vector DB', 'RAG', 'Embeddings', 'Unstructured Data', 'Semantic'],
      summary: 'Stores high-dimensional vector embeddings of enterprise SOPs, flood contingency protocols, and clinical service guidelines to ground AI agents without hallucination.',
      metrics: { vectorDimensions: 1536, indexedDocs: 12400, searchLatency: '18ms' },
      schemaSnippet: `// Hybrid Vector RAG Query via Data Cloud Search API
POST /api/v1/search/retrievers/SOP_ColdChain_Retriever/query
{
  "query": "Waterlogging protocol cold-chain temperature excursion Banjara Hills",
  "topK": 3,
  "filter": "Document_Type__c = 'Disaster_SOP'",
  "hybrid_weights": {
    "dense_vector": 0.7,
    "bm25_keyword": 0.3
  }
}`,
      explanation: 'Vector Search indexes unstructured PDFs, knowledge articles, and manuals. When an AI agent encounters a real-world exception, it retrieves chunked context with semantic similarity to ground reasoning.'
    },
    {
      id: 'b_calculated_insights',
      districtId: 'semantic',
      name: 'Calculated Insights Lighthouse',
      type: 'lighthouse',
      subtitle: 'Real-Time Cross-Cloud Aggregation & Care Risk Scores',
      floors: 55,
      gridX: 23,
      gridY: 4,
      width: 2,
      height: 2,
      color: '#155e75',
      roofType: 'beacon',
      relationships: ['b_data_lake', 'b_harmonizer', 'b_agentforce_core'],
      tags: ['Calculated Insights', 'SQL', 'Metrics', 'Real-Time Scoring', 'Streaming'],
      summary: 'Continuously aggregates cross-cloud metrics across billions of records, delivering real-time scores (such as Household Care Risk and Depot Grid Stress) directly to agents.',
      metrics: { activeCIs: 34, refreshFrequency: 'Streaming & 1-Hour Batch' },
      schemaSnippet: `// Calculated Insight SQL Definition
SELECT 
    UnifiedIndividual__dlm.Id__c as UnifiedId__c,
    MAX(INDRA_Shipment__dlm.Temp_Excursion__c) as MaxTempExcursion__c,
    COUNT(Case__dlm.Id__c) as RecentCasesCount__c,
    (COUNT(Case__dlm.Id__c) * 1.5 + MAX(INDRA_Shipment__dlm.Temp_Excursion__c) * 4.0) as HouseholdCareRiskScore__c
FROM UnifiedIndividual__dlm
JOIN INDRA_Shipment__dlm ON UnifiedIndividual__dlm.Id__c = INDRA_Shipment__dlm.ConsigneeId__c
GROUP BY UnifiedIndividual__dlm.Id__c`,
      explanation: 'Calculated Insights (CIs) run multi-dimensional SQL aggregation over petabytes of data, turning raw event streams into actionable numeric signals that trigger business flows and Agentforce reasoning loops.'
    },
    {
      id: 'b_headless_gateway',
      districtId: 'headless',
      name: 'Headless 360 API Gateway',
      type: 'skyport',
      subtitle: 'GraphQL, REST Composite & Composable Endpoints',
      floors: 42,
      gridX: 3,
      gridY: 15,
      width: 2,
      height: 2,
      color: '#10b981',
      roofType: 'helipad',
      relationships: ['b_security_fortress', 'b_events_hub', 'b_hxl_terminals'],
      tags: ['Headless 360', 'GraphQL', 'Composite API', 'The API is the UI', 'REST'],
      summary: 'The primary ingress/egress terminal liberating Salesforce data and business logic from the Lightning Experience DOM, powering zero-browser micro-frontends and mobile apps.',
      metrics: { avgRoundtrip: '48ms', throughputRps: '2,800', bandwidthSaved: '88%' },
      schemaSnippet: `// Headless 360 GraphQL Query: Multi-Object Single Roundtrip
query getConsigneeRescueContext($shipmentNumber: String!) {
  uiapi {
    query {
      INDRA_Shipment__c(where: { Shipment_Number__c: { eq: $shipmentNumber } }) {
        edges {
          node {
            Id
            Temp_Excursion_Flag__c { value }
            Consignee__r {
              Name { value }
              Phone { value }
            }
          }
        }
      }
    }
  }
}`,
      explanation: 'Headless 360 removes the heavy browser UI layer. Instead of downloading multi-megabyte JavaScript bundles for Lightning components, clients query exactly what they need in a single HTTP roundtrip.'
    },
    {
      id: 'b_hxl_terminals',
      districtId: 'headless',
      name: 'Headless Experience Layer (HXL)',
      type: 'docking_bays',
      subtitle: 'Slack Concierge, Mobile Ops & External AI Surfaces',
      floors: 30,
      gridX: 6,
      gridY: 18,
      width: 3,
      height: 2,
      color: '#059669',
      roofType: 'antennas_array',
      relationships: ['b_headless_gateway', 'b_agentforce_core', 'b_mcp_headless'],
      tags: ['HXL', 'Slack Bot', 'React Micro-Frontend', 'Mobile Console', 'Zero-UI'],
      summary: 'Outbound surfaces where human coworkers and AI agents collaborate seamlessly without ever logging into a traditional Salesforce browser tab.',
      metrics: { surfacesConnected: 6, slackUsers: 1400, mobileFleetDevices: 280 },
      schemaSnippet: `// Slack Socket Mode Event Handler (HXL Node)
slackApp.action('approve_shipment_reroute', async ({ ack, body, client }) => {
    await ack();
    // Dispatch direct tool call to Headless 360 without touching Salesforce UI
    const result = await headlessMcp.dispatch('execute_rescue_action', {
        caseId: body.actions[0].value,
        approverId: body.user.id
    });
    await client.chat.postMessage({
        channel: body.channel.id,
        text: '✅ Rescue flight dispatched! Tracking code: ' + result.trackingId
    });
});`,
      explanation: 'The Headless Experience Layer proves "The API is the UI". Operations teams manage mission-critical logistics entirely inside Slack, dedicated field tablet apps, or automated agent loops.'
    },
    {
      id: 'b_agentforce_core',
      districtId: 'agentforce',
      name: 'Atlas Reasoning Engine Spire',
      type: 'ai_spire',
      subtitle: 'Autonomous Perception, Topic Routing & Action Planning',
      floors: 72,
      gridX: 12,
      gridY: 12,
      width: 3,
      height: 3,
      color: '#8b5cf6',
      roofType: 'pulsing_orb',
      relationships: ['b_vector_vault', 'b_calculated_insights', 'b_trust_layer'],
      tags: ['Agentforce', 'Atlas Engine', 'Topics', 'Reasoning Loop', 'Autonomous'],
      summary: 'The cognitive heart of Agentforce. Continuously runs the Atlas loop: Perceives customer intent, evaluates guardrails, selects topics, grounds in Data Cloud, plans actions, and executes Apex tools.',
      metrics: { activeAgents: 4, tasksAutonomousPct: '88.4%', avgResolutionSec: 4.2 },
      schemaSnippet: `// Agentforce Atlas Topic & Action Definition (Metadata YAML)
agent:
  name: "Kaveri_Harbor_Care_Coworker"
  description: "Autonomous concierge handling cold-chain excursions and logistics disruptions."
  topics:
    - name: "ColdChain_Rescue"
      description: "Handles depot temperature spikes and flood rerouting."
      classification_rules:
        - "temp > 8C in transit"
        - "monsoon waterlogging alert"
      actions:
        - name: "Query_Unified_Household"
          target: "Data360_MCP.execute"
        - name: "Create_Rescue_Case"
          target: "Headless360_MCP.dispatch"
      guardrails:
        - "Do not commit financial compensation over $500 without supervisor"`,
      explanation: 'Unlike deterministic chatbots that follow rigid decision trees, the Atlas Reasoning Engine reasons dynamically. It breaks complex prompts down into a sequence of safe, governed tool invocations.'
    },
    {
      id: 'b_trust_layer',
      districtId: 'agentforce',
      name: 'Einstein Trust Layer Bastion',
      type: 'shield_dome',
      subtitle: 'Zero Data Retention, PII Masking & Toxicity Defense',
      floors: 25,
      gridX: 10,
      gridY: 15,
      width: 2,
      height: 2,
      color: '#7c3aed',
      roofType: 'forcefield',
      relationships: ['b_agentforce_core', 'b_claudeforce_lab', 'b_security_fortress'],
      tags: ['Trust Layer', 'PII Masking', 'Zero Retention', 'Audit Trail', 'Guardrails'],
      summary: 'Enterprise security perimeter wrapping all generative and agentic model calls. Strips sensitive PII before model transmission, prevents model training, and logs every reasoning step.',
      metrics: { piiEntitiesMasked: '1.2M', toxicityBlocks: 42, auditCompliance: '100%' },
      schemaSnippet: `// Einstein Trust Layer Pipeline
1. Inbound Request -> Detect PII (SSN, Credit Card, Medical ID)
2. Mask with Secure Synthetic Tokens: "Dr. [NAME_1] at [ADDR_2]"
3. Check Harm & Toxicity Classifier (Score < 0.05)
4. Dynamic Grounding: Inject RAG chunks from Data Cloud Vector Vault
5. Enforce Zero-Retention Agreement with LLM Gateway
6. De-mask tokens in final response & log full audit trail to BigObject`,
      explanation: 'The Einstein Trust Layer guarantees that enterprise customer data is never used to train external LLMs, ensuring strict adherence to HIPAA, GDPR, and enterprise NDA agreements.'
    },
    {
      id: 'b_claudeforce_lab',
      districtId: 'claudeforce',
      name: 'Claude 3.5 Cognitive Observatory',
      type: 'observatory',
      subtitle: 'Deep Architectural Reasoning, SOQL Synthesis & Multi-Modal',
      floors: 60,
      gridX: 17,
      gridY: 13,
      width: 2,
      height: 2,
      color: '#f97316',
      roofType: 'rotating_dome',
      relationships: ['b_agentforce_core', 'b_apex_foundry', 'b_trust_layer'],
      tags: ['Claudeforce', 'Claude 3.5 Sonnet', 'Multi-Modal', 'Code Generation', 'Reasoning'],
      summary: 'Anthropic Claude integration with Salesforce. Excels at processing 200k context windows of messy enterprise documents, refactoring legacy Apex, and generating performant SOQL.',
      metrics: { contextWindow: '200,000 tokens', apexGenerationAccuracy: '98.6%', visionLatency: '820ms' },
      schemaSnippet: `// Claudeforce Agentic Multi-Modal Workflow (Prompt + Vision)
const result = await anthropic.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 4096,
    system: "You are Claudeforce, an elite Salesforce Technical Architect. Enforce WITH USER_MODE, bulkification, and SOQL governor limits in all generated code.",
    messages: [{
        role: "user",
        content: [
            { type: "text", text: "Parse this bill of lading photo and verify cold-chain compliance:" },
            { type: "image", source: { type: "base64", media_type: "image/jpeg", data: bolImageBase64 } }
        ]
    }]
});`,
      explanation: 'Claudeforce leverages Claude 3.5 Sonnet\'s frontier intelligence for complex enterprise scenarios: parsing handwritten shipping manifests, cross-referencing multi-page contracts, and auditing Apex triggers for governor limit violations.'
    },
    {
      id: 'b_mcp_context',
      districtId: 'mcp',
      name: 'Plane 1: Data 360 MCP Server',
      type: 'maglev_terminal',
      subtitle: 'System of Context [search | payload_examples | execute]',
      floors: 48,
      gridX: 20,
      gridY: 17,
      width: 2,
      height: 2,
      color: '#ec4899',
      roofType: 'maglev_track',
      relationships: ['b_data_lake', 'b_harmonizer', 'b_agentforce_core'],
      tags: ['MCP', 'Data 360', 'System of Context', 'search', 'execute'],
      summary: 'Hosted Model Context Protocol server exposing the entire enterprise semantic layer (DLOs, DMOs, Identity Resolution, and Calculated Insights) as standardized LLM tools.',
      metrics: { toolsExposed: 3, endpoint: 'api.salesforce.com/platform/mcp/v1/data/data360', status: 'GA' },
      schemaSnippet: `// Plane 1: Data 360 MCP Server Meta-Tools
1. "data360_search":
   Query available DMOs, Calculated Insights, and Semantic models.
2. "data360_payload_examples":
   Inspect sample schemas and query parameters for selected models.
3. "data360_execute":
   Execute parameterized SQL/GraphQL queries against the Data 360 graph.`,
      explanation: 'Plane 1 acts as the System of Context. When an AI client needs to understand customer background, household relationships, or real-time metrics, it queries the Data 360 MCP server.'
    },
    {
      id: 'b_mcp_headless',
      districtId: 'mcp',
      name: 'Plane 2: Headless 360 MCP Server',
      type: 'maglev_terminal',
      subtitle: 'System of Action [discover | describe | dispatch]',
      floors: 48,
      gridX: 16,
      gridY: 20,
      width: 2,
      height: 2,
      color: '#db2777',
      roofType: 'maglev_track',
      relationships: ['b_security_fortress', 'b_apex_foundry', 'b_agentforce_core'],
      tags: ['MCP', 'Headless 360', 'System of Action', 'dispatch', 'FLS Enforced'],
      summary: 'Hosted Model Context Protocol server exposing Salesforce platform capabilities (SObjects, Apex, Flows, Platform Events) as action tools, running strictly as the authenticated user.',
      metrics: { toolsExposed: 4, endpoint: 'api.salesforce.com/platform/mcp/v1/platform/headless-360', status: 'Beta' },
      schemaSnippet: `// Plane 2: Headless 360 MCP Server Meta-Tools
1. "headless360_discover":
   List available actions, SObjects, and invocable flows accessible to user.
2. "headless360_describe":
   Get typed parameter schemas for a target SObject or Apex invocable.
3. "headless360_dispatch":
   Execute state-modifying actions (insert, update, flow call, publish event).
4. "headless360_dispatch_readonly":
   Execute read-only SOQL queries with compile-time security.`,
      explanation: 'Plane 2 acts as the System of Action. Collapsing Plane 1 and Plane 2 is an architectural anti-pattern. While Plane 1 reads context, Plane 2 executes governed actions under strict user FLS, sharing rules, and audit logging.'
    }
  ],

  // Data conduits connecting buildings
  conduits: [
    { from: 'b_standard_objects', to: 'b_custom_objects', type: 'metadata', label: 'Lookup / Master-Detail Rel' },
    { from: 'b_standard_objects', to: 'b_security_fortress', type: 'metadata', label: 'FLS & Sharing Boundary' },
    { from: 'b_custom_objects', to: 'b_apex_foundry', type: 'automation', label: 'Trigger Pipeline' },
    { from: 'b_flow_powerhouse', to: 'b_events_hub', type: 'automation', label: 'Platform Event Fire' },
    { from: 'b_apex_foundry', to: 'b_flow_powerhouse', type: 'automation', label: 'Invocable Apex Calls' },
    { from: 'b_custom_objects', to: 'b_data_lake', type: 'semantic', label: 'Data Ingestion Stream' },
    { from: 'b_data_lake', to: 'b_harmonizer', type: 'semantic', label: 'DLO -> DMO Harmonize' },
    { from: 'b_harmonizer', to: 'b_calculated_insights', type: 'semantic', label: 'Continuous Aggregation' },
    { from: 'b_harmonizer', to: 'b_vector_vault', type: 'semantic', label: 'Vector RAG Embeddings' },
    { from: 'b_vector_vault', to: 'b_agentforce_core', type: 'agentforce', label: 'Context Grounding' },
    { from: 'b_calculated_insights', to: 'b_agentforce_core', type: 'agentforce', label: 'Care Risk Score Triggers' },
    { from: 'b_agentforce_core', to: 'b_trust_layer', type: 'agentforce', label: 'Guardrail & Masking Gate' },
    { from: 'b_agentforce_core', to: 'b_claudeforce_lab', type: 'claudeforce', label: 'Frontier Co-Pilot Request' },
    { from: 'b_agentforce_core', to: 'b_mcp_context', type: 'mcp', label: 'Plane 1 Read Context' },
    { from: 'b_agentforce_core', to: 'b_mcp_headless', type: 'mcp', label: 'Plane 2 Dispatch Action' },
    { from: 'b_mcp_headless', to: 'b_headless_gateway', type: 'headless', label: 'Headless 360 Dispatch' },
    { from: 'b_headless_gateway', to: 'b_hxl_terminals', type: 'headless', label: 'Slack & Mobile HXL' }
  ],

  simulations: [
    {
      id: 'sim_cold_chain_rescue',
      title: 'Monsoon Cold-Chain Emergency Rescue',
      badge: 'Agentforce + Dual MCPs',
      description: 'IoT sensor detects 9.2°C temperature spike on Biologics shipment. Demonstrates Data 360 event ingestion -> Atlas reasoning loop -> Headless 360 MCP dispatch -> Slack Concierge notification.',
      steps: [
        {
          district: 'semantic',
          buildingId: 'b_data_lake',
          action: '1. Ingest IoT Excursion Stream',
          detail: 'Sensor DC-HYD-04 records 9.2°C (exceeding 8°C threshold) for Shipment SH-88392.'
        },
        {
          district: 'semantic',
          buildingId: 'b_harmonizer',
          action: '2. Identity Resolution Match',
          detail: 'Harmonizes consignee to Dr. Meera Reddy (Household node) with Critical SLA.'
        },
        {
          district: 'automation',
          buildingId: 'b_events_hub',
          action: '3. Kafka Event Bus Broadcast',
          detail: 'Data Action publishes INDRA_Care_Signal__e to Kafka Event Bus.'
        },
        {
          district: 'agentforce',
          buildingId: 'b_agentforce_core',
          action: '4. Atlas Reasoning Engine Execution',
          detail: 'Agent Kaveri assesses ColdChain_Rescue topic, evaluates GHMC flood SOPs via Vector RAG.'
        },
        {
          district: 'mcp',
          buildingId: 'b_mcp_headless',
          action: '5. Headless 360 MCP Tool Dispatch',
          detail: 'Calls headless360_dispatch to insert P0 Care Case and dispatch drone courier.'
        },
        {
          district: 'headless',
          buildingId: 'b_hxl_terminals',
          action: '6. Outbound Slack Notification',
          detail: 'Interactive Slack notification sent to #harbor-care with 1-click rescue approval.'
        }
      ]
    },
    {
      id: 'sim_claudeforce_audit',
      title: 'Claudeforce Multi-Modal Manifest Triage',
      badge: 'Claude 3.5 + Governed Apex',
      description: 'Carrier uploads handwritten bill of lading. Claude 3.5 Sonnet extracts cold-chain certifications, writes Apex unit tests, and validates compliance against Data Cloud standards.',
      steps: [
        {
          district: 'claudeforce',
          buildingId: 'b_claudeforce_lab',
          action: '1. Multi-Modal Vision Ingestion',
          detail: 'Claude 3.5 Sonnet parses handwritten dry-ice manifest and extracts batch serials.'
        },
        {
          district: 'semantic',
          buildingId: 'b_vector_vault',
          action: '2. RAG Regulatory Cross-Check',
          detail: 'Retrieves FDA & DGCA cold-chain transit regulations from Vector Vault.'
        },
        {
          district: 'automation',
          buildingId: 'b_apex_foundry',
          action: '3. Generate WITH USER_MODE Apex',
          detail: 'Synthesizes bulkified Apex verification handler with 100% test coverage.'
        },
        {
          district: 'metadata',
          buildingId: 'b_security_fortress',
          action: '4. FLS & Trust Perimeter Audit',
          detail: 'Verifies compile-time field permissions and logs to Setup Audit Trail.'
        }
      ]
    }
  ]
};
'''

with open('/Users/asmgkr/.gemini/antigravity/scratch/salesforce-city-visualizer/src/data/metadataCatalog.js', 'w') as f:
    f.write(metadata_catalog_code)

print("metadataCatalog.js written successfully!")
