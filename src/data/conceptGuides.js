export const CONCEPT_GUIDES = {
  headless360: {
    id: 'headless360',
    title: 'Headless 360: The API is the UI',
    subtitle: 'Decoupling Customer 360 from the Browser DOM',
    tagline: '"No browser required. High-performance, composable, agent-first CRM."',
    icon: '🚀',
    accentColor: '#10b981',
    summary: 'Headless 360 is the architectural paradigm of decoupling Salesforce data, customer context, and transactional business logic from the traditional Salesforce Lightning Experience (LEX) browser interface.',
    
    whyItMatters: [
      {
        title: 'Zero-Browser Latency',
        description: 'Traditional LEX pages transfer 12–18MB of JavaScript bundles, CSS stylesheets, and Aura/LWC components, resulting in 2-5 second rendering delays. Headless 360 APIs respond in 30-50 milliseconds with exact JSON payloads.'
      },
      {
        title: 'Native AI Agent Readiness',
        description: 'Autonomous AI agents (Agentforce, Claude, Gemini) cannot reliably interact with dynamic DOM buttons, dropdowns, and iframes. Headless 360 exposes typed, deterministic APIs and MCP tools that agents execute with mathematical precision.'
      },
      {
        title: 'Bespoke Frontline Surfaces',
        description: 'Empowers logistics coordinators in Slack, depot managers on rugged Android scanners, and e-commerce shoppers on Next.js composable storefronts to interact with Salesforce without ever logging into a Salesforce tab.'
      }
    ],

    fourLayers: [
      {
        layer: 'Layer 4: Headless Experience Layer (HXL)',
        color: '#10b981',
        components: 'Slack Channels, React Micro-Frontends, Native iOS/Android Fleet Consoles, External AI Agents (Claude / Gemini).',
        description: 'Omnichannel presentation layer where human coworkers and AI agents collaborate. Interacts strictly via HTTP/2, WebSocket, and MCP.'
      },
      {
        layer: 'Layer 3: Orchestration Plane',
        color: '#8b5cf6',
        components: 'Agentforce Atlas Reasoning Engine, Prompt Templates, Guardrails, MuleSoft Agent Fabric.',
        description: 'Decides what business actions to take. Classifies customer intent, selects topics, and orchestrates calls between context and action systems.'
      },
      {
        layer: 'Layer 2: Business Logic & Platform Plane',
        color: '#eab308',
        components: 'Apex Services (WITH USER_MODE), Autolaunched Flows, Platform Events, CDC Relays, Headless 360 MCP Server.',
        description: 'Enforces transactional integrity, Field-Level Security (FLS), Sharing Rules, and governor limits. Executes state updates and publishes change events.'
      },
      {
        layer: 'Layer 1: Data 360 — System of Context',
        color: '#06b6d4',
        components: 'Data Lake Objects (DLOs), Harmonized DMOs, Identity Resolution, Calculated Insights, Vector RAG Retrievers.',
        description: 'Unified customer graph bridging CRM records, real-time IoT telemetry, Zero-Copy lakehouse tables, and unstructured SOP knowledge.'
      }
    ],

    comparison: {
      monolith: {
        title: 'Traditional Monolithic CRM (LEX)',
        payloadSize: '14.8 MB',
        loadTime: '2,800 ms',
        flexibility: 'Rigid standard UI flexipages',
        agentUsability: 'Extremely poor (brittle DOM scrapers)',
        costPerInteraction: 'High compute + full user seat licensing'
      },
      headless: {
        title: 'Headless 360 Composable Architecture',
        payloadSize: '2.4 KB (GraphQL / JSON)',
        loadTime: '42 ms',
        flexibility: '100% composable (Slack, Mobile, Web, Watch)',
        agentUsability: 'Native (Direct Model Context Protocol & Tools)',
        costPerInteraction: 'Ultra-low (API / Flex Credit token consumption)'
      }
    },

    sampleCode: {
      title: 'Headless 360 GraphQL Query',
      lang: 'graphql',
      code: `query GetColdChainRescuePayload($shipmentId: ID!) {
  uiapi {
    query {
      INDRA_Shipment__c(where: { Id: { eq: $shipmentId } }) {
        edges {
          node {
            Id
            Temp_Celsius__c { value }
            Priority__c { value }
            Consignee__r {
              Name { value }
              Phone { value }
              Unified_Household_Id__c { value }
            }
          }
        }
      }
    }
  }
}`
    }
  },

  agentforce: {
    id: 'agentforce',
    title: 'Agentforce (Aiforce) & The Atlas Engine',
    subtitle: 'Autonomous Enterprise AI Coworkers with Guardrails',
    tagline: '"Beyond deterministic bots: Continuous reasoning, grounding, and governed action."',
    icon: '🤖',
    accentColor: '#8b5cf6',
    summary: 'Agentforce is Salesforce\'s autonomous AI platform. Rather than following brittle if-then branching trees, Agentforce uses the Atlas Reasoning Engine to plan, ground, and execute business actions 24/7.',

    atlasCycle: [
      {
        step: '1. Perception & Intent Ingestion',
        icon: '👂',
        description: 'Continuously listens to customer inquiries across Slack, WhatsApp, SMS, or automated IoT sensor alerts.'
      },
      {
        step: '2. Trust Layer Guardrail Scan',
        icon: '🛡️',
        description: 'Masks sensitive PII (SSN, credit card, medical identifiers), evaluates toxicity, and validates safety boundaries.'
      },
      {
        step: '3. Topic Classification',
        icon: '🎯',
        description: 'Dynamically routes the prompt to an enterprise Topic (e.g. ColdChain_Rescue, Order_Reroute, Billing_Dispute) with locked scope.'
      },
      {
        step: '4. Semantic Context Grounding',
        icon: '🌐',
        description: 'Queries Data Cloud to retrieve the Unified Individual Golden Record, real-time Calculated Insights, and Vector RAG chunks.'
      },
      {
        step: '5. Action Planning & Invocable Dispatch',
        icon: '⚡',
        description: 'Plans a deterministic sequence of Apex Invocable Methods, Autolaunched Flows, or Headless 360 MCP tool calls.'
      },
      {
        step: '6. Output & Audit Logging',
        icon: '📝',
        description: 'Returns the governed resolution to the customer surface and logs an immutable audit entry to Salesforce BigObjects.'
      }
    ],

    keyDifferentiators: [
      {
        title: 'Deterministic Guardrails with Non-Deterministic Reasoning',
        detail: 'The LLM reasons flexibly over human intent, but the actions it can take are strictly gated by typed Salesforce Apex/Flow contracts.'
      },
      {
        title: 'Unified Customer Grounding',
        detail: 'Never hallucinates customer status because it is grounded in Data Cloud\'s unified identity graph and calculated metrics.'
      },
      {
        title: 'Zero Data Retention (ZDR)',
        detail: 'The Einstein Trust Layer guarantees customer data is never stored by or used to train third-party foundation models.'
      }
    ],

    sampleCode: {
      title: 'Invocable Apex Action for Agentforce',
      lang: 'apex',
      code: `public with sharing class INDRA_ColdChainRescueAction {
    public class Request {
        @InvocableVariable(required=true label='Shipment ID')
        public Id shipmentId;
        @InvocableVariable(required=true label='Current Temp Celsius')
        public Decimal currentTemp;
    }

    public class Response {
        @InvocableVariable(label='Rescue Case ID')
        public Id caseId;
        @InvocableVariable(label='Is Rerouted')
        public Boolean isRerouted;
    }

    @InvocableMethod(label='Dispatch Autonomous Cold-Chain Rescue' category='Agentforce')
    public static List<Response> execute(List<Request> requests) {
        List<Response> resList = new List<Response>();
        for (Request req : requests) {
            // Apex executes securely WITH USER_MODE
            INDRA_Care_Case__c c = new INDRA_Care_Case__c(
                Shipment__c = req.shipmentId,
                Status__c = 'Dispatched_Autonomous'
            );
            insert as user c;
            Response r = new Response();
            r.caseId = c.Id;
            r.isRerouted = true;
            resList.add(r);
        }
        return resList;
    }
}`
    }
  },

  claudeforce: {
    id: 'claudeforce',
    title: 'Claudeforce: Claude 3.5 + Salesforce',
    subtitle: 'Frontier Intelligence for Enterprise Architecture & Automation',
    tagline: '"200k context, multimodal document comprehension, and governed code generation."',
    icon: '🧠',
    accentColor: '#f97316',
    summary: 'Claudeforce embodies the deep synergy between Anthropic Claude 3.5 Sonnet / Haiku and Salesforce CRM. It delivers architectural reasoning, multi-modal document intelligence, and enterprise-grade code synthesis.',

    corePowers: [
      {
        title: '200,000 Token Context Window',
        description: 'Ingest an entire Salesforce org\'s schema, metadata relationships, and 50+ Apex classes in a single prompt to audit architecture or identify anti-patterns.'
      },
      {
        title: 'Multi-Modal Vision Understanding',
        description: 'Parse messy handwritten bills of lading, customs clearance stamps, cold-chain temperature strip charts, and warehouse damage photos directly into structured SObject records.'
      },
      {
        title: 'Governor-Compliant Code Synthesis',
        description: 'Generates robust Apex code strictly complying with Salesforce multi-tenant limits: 100 SOQL queries, 150 DML statements, bulkification, and modern WITH USER_MODE syntax.'
      },
      {
        title: 'Natural Language to Optimized SOQL',
        description: 'Converts complex business questions ("Which high-value accounts in Hyderabad had shipments delayed by rain this week?") into index-optimized SOQL queries with selective WHERE clauses.'
      }
    ],

    workflowExample: [
      { step: 'Step 1: Manifest Upload', text: 'Truck driver snaps a smartphone photo of physical BOL with dry-ice log.' },
      { step: 'Step 2: Claude Multi-Modal Parse', text: 'Claude 3.5 Sonnet extracts batch serials, origin lab, expiry timestamps, and certifies signatures.' },
      { step: 'Step 3: Schema Mapping', text: 'Synthesizes JSON payload matching INDRA_Shipment__c and ColdChain_Reading__c custom fields.' },
      { step: 'Step 4: Tool Execution', text: 'Dispatches payload via Headless 360 MCP server with compile-time security.' }
    ],

    sampleCode: {
      title: 'Claudeforce Prompt Grounding Template',
      lang: 'json',
      code: `{
  "model": "claude-3-5-sonnet-20241022",
  "system": "You are Claudeforce. Follow Salesforce Apex & Data Cloud architectural standards. Always use WITH USER_MODE, bulkified collections, and avoid SOQL inside loops.",
  "messages": [
    {
      "role": "user",
      "content": "Refactor this legacy before-update trigger into a modern domain-driven handler with Platform Event publishing."
    }
  ]
}`
    }
  },

  mcpApis: {
    id: 'mcpApis',
    title: 'Dual-Plane MCPs & Modern Salesforce APIs',
    subtitle: 'The Model Context Protocol Standard for Enterprise AI',
    tagline: '"Two distinct hosted planes: System of Context vs. System of Action."',
    icon: '🔌',
    accentColor: '#ec4899',
    summary: 'The Model Context Protocol (MCP) is the open standard that connects AI models to external tools and context. Salesforce provides a Dual-Plane hosted MCP architecture to guarantee enterprise security.',

    dualPlanes: [
      {
        plane: 'Plane 1: Data 360 MCP Server (data360)',
        subtitle: 'System of Context',
        color: '#06b6d4',
        endpoint: 'https://api.salesforce.com/platform/mcp/v1/data/data360',
        status: 'General Availability (GA)',
        tools: [
          'data360_search: Discover available DMOs, Calculated Insights, and Semantic models.',
          'data360_payload_examples: Inspect sample query schemas and parameters.',
          'data360_execute: Run parameterized SQL/GraphQL context queries.'
        ],
        security: 'Data space isolation, View/Manage Data 360 permissions, read-only analytics isolation.',
        whySeparate: 'Keeps massive analytical reads isolated from transactional state-changing mutations.'
      },
      {
        plane: 'Plane 2: Headless 360 MCP Server (platform/headless-360)',
        subtitle: 'System of Action (Platform Execution Plane)',
        color: '#db2777',
        endpoint: 'https://api.salesforce.com/platform/mcp/v1/platform/headless-360',
        status: 'Beta (v67.0+)',
        tools: [
          'headless360_discover: Catalog accessible SObjects, Flows, and Apex actions.',
          'headless360_describe: Retrieve typed parameter schemas for a target action.',
          'headless360_dispatch: Execute state-changing actions (insert, update, flow call).',
          'headless360_dispatch_readonly: Run secure SOQL queries with user mode.'
        ],
        security: 'Strictly executes as authenticated user; native FLS, CRUD, and sharing rules enforced. Writes to Setup Audit Trail.',
        whySeparate: 'Prevents privilege escalation; guarantees that every tool call adheres to the user\'s exact CRM permissions.'
      }
    ],

    apiLandscape: [
      {
        name: 'GraphQL API',
        type: 'Query & Mutation',
        bestFor: 'Single-roundtrip multi-object queries for mobile apps and Headless 360 micro-frontends with zero over-fetching.'
      },
      {
        name: 'REST Composite & Graph',
        type: 'Transactional Batch',
        bestFor: 'Executing up to 500 dependent sub-requests atomically with rollback-on-error support.'
      },
      {
        name: 'Pub/Sub API (gRPC)',
        type: 'Streaming Events',
        bestFor: 'Bi-directional streaming of Platform Events and Change Data Capture (CDC) over HTTP/2 with high throughput.'
      },
      {
        name: 'Tooling & Metadata API',
        type: 'DevOps & Administration',
        bestFor: 'Dynamic inspection of org configuration, custom fields, Apex classes, and CI/CD deployment pipelines.'
      },
      {
        name: 'Bulk API 2.0',
        type: 'High-Volume Data Loading',
        bestFor: 'Asynchronous ingestion of millions of records with automated chunking and parallel processing.'
      }
    ],

    sampleCode: {
      title: 'MCP Client Tool Call to Headless 360',
      lang: 'json',
      code: `// MCP JSON-RPC 2.0 Tool Call
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "headless360_dispatch",
    "arguments": {
      "action": "insert_record",
      "sObjectType": "INDRA_Care_Case__c",
      "fields": {
        "Shipment__c": "a018800000XyZ1A",
        "Severity__c": "Critical_P0",
        "Subject": "Autonomous Cold-Chain Reroute"
      }
    }
  },
  "id": "call-0941"
}`
    }
  },

  semanticMatrix: {
    id: 'semanticMatrix',
    title: 'The Metadata & Semantic Layer Matrix',
    subtitle: 'From Database Tables to Ontological Customer Knowledge',
    tagline: '"How Salesforce bridges raw relational data, declarative metadata, and AI ontologies."',
    icon: '🏢',
    accentColor: '#3b82f6',
    summary: 'Understanding a Salesforce org requires distinguishing between three evolutionary tiers: the physical database layer, the declarative metadata layer, and the semantic ontologies of Data Cloud.',

    tiers: [
      {
        tier: 'Tier 1: Physical Relational Storage',
        metaphor: 'The Foundation Piles',
        technology: 'Oracle / PostgreSQL Multi-Tenant Database',
        content: 'Raw tables with partitioned org IDs, custom field columns (Value0, Value1), and clustered indexes.',
        visibility: 'Hidden from developers behind the Salesforce abstraction.'
      },
      {
        tier: 'Tier 2: Declarative Metadata Layer',
        metaphor: 'The Structural Skyscraper Framework',
        technology: 'SObjects, Custom Fields, Layouts, FLS, Sharing Rules, Apex, Flows',
        content: 'Declarative XML/JSON metadata representations. Defines what an Account or Shipment is, who can see it, and what happens when it changes.',
        visibility: 'Admin and Developer domain (Setup, VS Code, SFDX).'
      },
      {
        tier: 'Tier 3: The Semantic Layer (Data Cloud / Ontologies)',
        metaphor: 'The Smart City Brain & Unified Graph',
        technology: 'Cloud Information Model (CIM), DLOs, DMOs, Identity Resolution, Vectors',
        content: 'Business meaning above physical schema. Unifies fragmented identities into a single human, indexes semantic meanings into vector space, and calculates live customer metrics.',
        visibility: 'Agentforce, Claude, Analytics, and Headless 360 consumers.'
      }
    ]
  }
};
