#%%
import json, csv

dataset = []

def add(qid, question, docs, category, difficulty, answerable, reference_answer, evidence):
    dataset.append({
        "id": qid,
        "question": question,
        "expected_documents": docs,
        "category": category,
        "difficulty": difficulty,
        "answerable": answerable,
        "reference_answer": reference_answer,
        "evidence_keywords": evidence
    })


# ---------------- PRA SS1/23: 12 ----------------
add("PRA-01", "What is the PRA's definition of a model, and what kinds of inputs and outputs does the definition cover?",
    ["PRA SS1/23"], "definition", "easy", True,
    "A model is a quantitative method, system or approach applying statistical, economic, financial or mathematical theories, techniques and assumptions to process input data into output. Inputs and outputs may be quantitative or qualitative, and inputs may also be expert-judgement based.",
    ["quantitative method", "statistical", "economic", "financial", "mathematical", "expert judgement", "quantitative", "qualitative"])

add("PRA-02", "Why does the PRA expect firms to maintain a model inventory?",
    ["PRA SS1/23"], "governance", "easy", True,
    "The model inventory helps firms identify sources of model risk, provide management information for reporting model risk, and identify model inter-dependencies.",
    ["model inventory", "sources of model risk", "management information", "inter-dependencies"])

add("PRA-03", "What is the purpose of a risk-based model tiering approach under SS1/23?",
    ["PRA SS1/23"], "governance", "easy", True,
    "The tiering approach categorises models to help identify and manage model risk, with validation intensity and rigour aligned to the model's risk/materiality.",
    ["risk-based tiering", "categorise models", "manage model risk", "validation"])

add("PRA-04", "What responsibilities does SS1/23 assign to model owners regarding model performance monitoring?",
    ["PRA SS1/23"], "governance", "medium", True,
    "Model owners are accountable for ensuring model performance is monitored against the firm's board-approved risk appetite for acceptable model performance, among other lifecycle responsibilities.",
    ["model owners", "performance monitoring", "board-approved risk appetite"])

add("PRA-05", "What does SS1/23 expect from the independence and expertise of model validation staff?",
    ["PRA SS1/23"], "validation", "medium", True,
    "Validators should have the technical expertise and sufficient familiarity with the relevant line of business to provide an objective, unbiased and critical opinion, together with sufficient organisational standing and incentives to report limitations.",
    ["technical expertise", "line of business", "objective", "unbiased", "critical opinion", "organisational standing"])

add("PRA-06", "What does Principle 3 of SS1/23 require firms to do during model development and use?",
    ["PRA SS1/23"], "development", "medium", True,
    "Firms should have a robust model development process covering design and implementation, model selection and performance measurement, with regular testing of data, model construct, assumptions and outcomes to identify, monitor, record and remediate limitations and weaknesses.",
    ["Principle 3", "model development", "implementation", "assumptions", "model outcomes", "remediate"])

add("PRA-07", "How does SS1/23 distinguish responsibility for model performance monitoring from responsibility for validation?",
    ["PRA SS1/23"], "governance", "hard", True,
    "Performance monitoring may be undertaken by model owners, users or developers, but its adequacy is a key consideration for model validators; validation itself should be performed by appropriately independent staff.",
    ["performance monitoring", "model owners", "users", "developers", "validators", "independence"])

add("PRA-08", "What does the PRA expect firms to do with their self-assessments and remediation plans under SS1/23?",
    ["PRA SS1/23"], "governance", "medium", True,
    "Firms are expected to conduct an initial self-assessment, update self-assessments at least annually, and review and update remediation plans regularly. Findings and remediation plans should be documented and shared with the board in a timely manner.",
    ["self-assessment", "at least annually", "remediation plans", "board"])

add("PRA-09", "A bank uses a deterministic algorithm rather than a statistical model, but the algorithm materially influences a complex business decision. Does SS1/23 say it can simply be excluded from model risk management?",
    ["PRA SS1/23"], "edge_case", "hard", True,
    "No. The PRA says that material deterministic quantitative methods that are not classified as models should still be considered for application of relevant MRM aspects where they materially affect business decisions and are complex; their implementation and use should at least have sound, documented management controls.",
    ["deterministic quantitative methods", "material", "business decisions", "complex", "management controls"])

add("PRA-10", "Does SS1/23 say that its expectations are conditions for receiving internal model approval?",
    ["PRA SS1/23"], "negative", "medium", True,
    "No. The statement says the expectations are not conditions for internal model approval; firms receiving permission to use an internal model for regulatory capital have 12 months from approval to comply with the policy.",
    ["not conditions", "internal model approval", "12 months"])

add("PRA-11", "What does SS1/23 say about models used for financial reporting and the audit committee?",
    ["PRA SS1/23"], "governance", "medium", True,
    "The PRA considers effective MRM for financial reporting relevant to the auditor's assessment of material misstatement and expects a report on MRM effectiveness for financial reporting to be available to the audit committee regularly and at least annually.",
    ["financial reporting", "material misstatement", "audit committee", "at least annually"])

add("PRA-12", "What model-lifecycle stages are explicitly covered by the high-level principles in SS1/23?",
    ["PRA SS1/23"], "lifecycle", "easy", True,
    "The five high-level principles are designed to cover all elements of the model lifecycle, including identification and classification, development/implementation/use, validation, governance and related controls.",
    ["five high-level principles", "model lifecycle", "identification", "development", "validation", "governance"])


# ---------------- SR 11-7: 12 ----------------
add("SR-01", "What are the three core elements of a comprehensive model validation framework in SR 11-7?",
    ["SR 11-7"], "validation", "easy", True,
    "Evaluation of conceptual soundness, ongoing monitoring including process verification and benchmarking, and outcomes analysis including back-testing.",
    ["conceptual soundness", "ongoing monitoring", "benchmarking", "outcomes analysis", "back-testing"])

add("SR-02", "Why does SR 11-7 recommend sensitivity analysis during model development and validation?",
    ["SR 11-7"], "validation", "medium", True,
    "Sensitivity analysis tests how small changes in inputs and parameter values affect model outputs. Unexpectedly large changes can indicate instability, while varying multiple inputs can reveal unexpected interactions.",
    ["sensitivity analysis", "small changes", "inputs", "parameter values", "unstable", "interactions"])

add("SR-03", "How does SR 11-7 distinguish sensitivity analysis from stress testing?",
    ["SR 11-7"], "validation", "medium", True,
    "Sensitivity analysis examines the effect of changes in inputs or parameters, including interactions; stress testing examines model performance across a wide range of inputs and parameter values, including extreme values, to assess robustness and boundaries of performance.",
    ["sensitivity analysis", "stress testing", "extreme values", "robust"])

add("SR-04", "How often should a bank periodically review each model under SR 11-7?",
    ["SR 11-7"], "monitoring", "easy", True,
    "At least annually, and more frequently when warranted. Material model changes should also be subject to validation.",
    ["periodic review", "at least annually", "material changes", "validation"])

add("SR-05", "What two broad types of model risk does SR 11-7 identify?",
    ["SR 11-7"], "model_risk", "medium", True,
    "Model risk can arise from fundamental errors in a model or from inappropriate use of the model.",
    ["fundamental errors", "inappropriate use"])

add("SR-06", "What kinds of model-quality characteristics does SR 11-7 say can be used to assess model quality?",
    ["SR 11-7"], "validation", "medium", True,
    "The guidance identifies characteristics including precision, accuracy, discriminatory power, robustness, stability and reliability.",
    ["precision", "accuracy", "discriminatory power", "robustness", "stability", "reliability"])

add("SR-07", "What should a bank do when a model's outcomes consistently fall outside an acceptable error range?",
    ["SR 11-7"], "monitoring", "medium", True,
    "The guidance says the model should be redeveloped when outcomes consistently fall outside the acceptable range established through analysis of outcomes around expected or predicted values.",
    ["acceptable range", "outcomes", "redeveloped"])

add("SR-08", "How should a bank validate a vendor model when it cannot obtain full access to coding and implementation details?",
    ["SR 11-7"], "vendor_model", "hard", True,
    "The bank may need to rely more heavily on sensitivity analysis and benchmarking, while still validating its own use of the vendor product, documenting customization choices and assessing data and assumptions for relevance.",
    ["vendor", "coding", "implementation", "sensitivity analysis", "benchmarking", "customization"])

add("SR-09", "What does SR 11-7 expect banks to do if a vendor model is no longer available or supported?",
    ["SR 11-7"], "vendor_model", "medium", True,
    "Banks should maintain contingency plans for situations in which the vendor model is no longer available or cannot be supported by the vendor.",
    ["contingency plans", "vendor model", "no longer available"])

add("SR-10", "What is the role of internal audit in model risk management according to SR 11-7?",
    ["SR 11-7"], "governance", "hard", True,
    "Internal audit should assess the overall effectiveness of the model risk management framework rather than duplicate MRM activities. It should evaluate whether MRM is comprehensive, rigorous and effective, including governance, validation, documentation, inventory, limits and supporting data/systems.",
    ["internal audit", "overall effectiveness", "comprehensive", "rigorous", "effective", "not duplicate"])

add("SR-11", "Can a bank's business unit independently decide to continue using a model despite validation identifying serious weaknesses, without any control function involvement?",
    ["SR 11-7"], "governance", "hard", True,
    "No. The guidance describes risk-control responsibilities including effective challenge, communication of validation issues, and authority to restrict model use and monitor usage limits.",
    ["risk controls", "effective challenge", "restrict use", "model limitations"])

add("SR-12", "What does SR 11-7 say about validating the bank's own use of a third-party model?",
    ["SR 11-7"], "vendor_model", "medium", True,
    "Even when a model is supplied by a vendor, the bank is expected to validate its own use of the vendor product and assess applicability, limitations, data, assumptions and customization.",
    ["validate", "own use", "vendor", "applicability", "limitations"])


# ---------------- IFRS 9: 12 ----------------
add("IFRS-01", "How does IFRS 9 define expected credit losses?",
    ["IFRS 9"], "definition", "easy", True,
    "Expected credit losses are a probability-weighted estimate of credit losses, defined as the present value of all cash shortfalls over the expected life of the financial instrument.",
    ["probability-weighted", "credit losses", "present value", "cash shortfalls", "expected life"])

add("IFRS-02", "What is the key trigger for recognising lifetime expected credit losses under IFRS 9?",
    ["IFRS 9"], "impairment", "easy", True,
    "Lifetime expected credit losses are recognised when there has been a significant increase in credit risk since initial recognition.",
    ["lifetime expected credit losses", "significant increase", "credit risk", "initial recognition"])

add("IFRS-03", "Is actual default at the reporting date required before lifetime expected credit losses are recognised?",
    ["IFRS 9"], "impairment", "medium", True,
    "No. The assessment is based on a significant increase in the likelihood or risk of default since initial recognition, generally before the asset becomes credit-impaired or actually defaults.",
    ["not actual default", "likelihood", "risk of default", "credit-impaired"])

add("IFRS-04", "Why can the same absolute increase in default risk be more significant for a low-risk instrument than for a high-risk instrument?",
    ["IFRS 9"], "impairment", "hard", True,
    "The significance of the change depends on the instrument's initial risk of default. The same absolute change is more significant relative to a lower initial risk than to a higher initial risk.",
    ["initial risk", "absolute change", "lower initial risk", "more significant"])

add("IFRS-05", "How does IFRS 9 treat the passage of time when assessing significant increases in credit risk?",
    ["IFRS 9"], "impairment", "hard", True,
    "Because risk over the expected life generally decreases as an instrument approaches maturity when credit risk is unchanged, comparing absolute default risk without considering expected life can be misleading. Other qualitative factors may also need to be considered.",
    ["expected life", "passage of time", "maturity", "qualitative factors"])

add("IFRS-06", "What does IFRS 9 say about grouping financial instruments when assessing significant increases in credit risk?",
    ["IFRS 9"], "measurement", "medium", True,
    "Financial instruments may be grouped based on shared credit-risk characteristics. If an entity cannot group instruments appropriately, it should recognise lifetime expected credit losses on the portion of assets for which credit risk is deemed to have increased significantly.",
    ["group", "shared credit risk characteristics", "collective", "lifetime expected credit losses"])

add("IFRS-07", "What happens to the impairment assessment if a modification of a financial asset results in derecognition of the original asset?",
    ["IFRS 9"], "modification", "medium", True,
    "The modified asset is treated as a new financial asset for impairment purposes, with the modification date treated as the date of initial recognition. Typically the loss allowance starts at 12-month expected credit losses until lifetime recognition criteria are met, subject to the possibility that the new asset is credit-impaired at initial recognition.",
    ["derecognition", "new financial asset", "date of initial recognition", "12-month", "credit-impaired"])

add("IFRS-08", "If a financial asset is modified but not derecognised, is it automatically considered to have lower credit risk?",
    ["IFRS 9"], "modification", "medium", True,
    "No. The entity must assess whether credit risk has significantly increased since initial recognition using all reasonable and supportable information, including historical and forward-looking information.",
    ["not automatically", "lower credit risk", "reasonable and supportable", "historical", "forward-looking"])

add("IFRS-09", "What does IFRS 9 say about a single timely payment after a loan modification and the assessment of credit risk?",
    ["IFRS 9"], "modification", "hard", True,
    "One timely payment would not typically erase a history of missed or incomplete payments. The borrower would generally need to demonstrate consistently good payment behaviour over a period before credit risk is considered to have decreased.",
    ["single payment", "missed", "incomplete payments", "consistently good payment behaviour"])

add("IFRS-10", "Why can a credit loss exist even when an entity expects to receive the full contractual amount?",
    ["IFRS 9"], "measurement", "medium", True,
    "Because expected credit losses consider both the amount and timing of cash flows, receiving the full amount later than contractually due creates a cash shortfall in present-value terms.",
    ["amount and timing", "cash shortfall", "later", "contractually due"])

add("IFRS-11", "For a loan commitment, what change in risk is considered when applying the significant-increase-in-credit-risk assessment?",
    ["IFRS 9"], "loan_commitment", "medium", True,
    "The entity considers changes in the risk of default occurring on the loan to which the loan commitment relates.",
    ["loan commitment", "risk of default", "loan"])

add("IFRS-12", "Does IFRS 9 require a single approach to assessing significant increases in credit risk or measuring expected credit losses for all financial instruments?",
    ["IFRS 9"], "methodology", "medium", True,
    "No. The standard allows different approaches for different financial instruments when assessing significant increases in credit risk or measuring expected credit losses.",
    ["various approaches", "different financial instruments"])


# ---------------- EBA: 12 ----------------
add("EBA-01", "What was the main purpose of the EBA's IRB survey report?",
    ["EBA IRB modelling practices"], "purpose", "easy", True,
    "It provides an overview of modelling techniques used for estimating PD, LGD for non-defaulted and defaulted exposures, and ELBE, and assesses the impact of the Guidelines on PD, LGD and defaulted assets.",
    ["IRB survey", "PD", "LGD", "ELBE", "impact assessment"])

add("EBA-02", "What was the population and time point represented by the EBA IRB survey results?",
    ["EBA IRB modelling practices"], "dataset_scope", "medium", True,
    "The survey responses reflected modelling practices at the time of completion in January 2017 and covered approved models. The quantitative sample contained 102 institutions from 22 Member States.",
    ["January 2017", "102 institutions", "22 Member States", "approved models"])

add("EBA-03", "What distinction does the EBA report make between model development and calibration?",
    ["EBA IRB modelling practices"], "methodology", "medium", True,
    "Model development is the process leading to risk differentiation, while calibration is the process leading to appropriate risk quantification.",
    ["model development", "risk differentiation", "calibration", "risk quantification"])

add("EBA-04", "Does the EBA report require the default definition used for PD model development to be identical to the CRR definition?",
    ["EBA IRB modelling practices"], "methodology", "hard", True,
    "No. The report explains that the development definition need not be identical to the CRR definition, provided consistency is maintained during the observation period and the definition does not negatively affect risk differentiation and predictive power. The definition used for risk quantification is required to be consistent with the CRR definition.",
    ["development", "default definition", "CRR", "risk differentiation", "risk quantification"])

add("EBA-05", "What was the reported share of PD models using a default definition different from the CRR definition during model development?",
    ["EBA IRB modelling practices"], "table", "medium", True,
    "18% of PD models in the survey used a definition different from the CRR definition during model development, corresponding to 44 of 242 models in the reported table.",
    ["18%", "44", "242", "PD models"])

add("EBA-06", "What is the purpose of calibration to the long-run average default rate according to the EBA report?",
    ["EBA IRB modelling practices"], "calibration", "medium", True,
    "Calibration is intended to ensure that, for a calibration segment, PD estimates in the calibration sample correspond to the long-run average default rate at the level relevant for the applied calibration method.",
    ["long-run average DR", "PD estimates", "calibration segment"])

add("EBA-07", "How can portfolio-level versus grade-level calibration affect rating migrations and cyclicality?",
    ["EBA IRB modelling practices"], "calibration", "hard", True,
    "With portfolio-level calibration, obligors can migrate across grades during recalibration. With grade/pool-level calibration combined with PIT rating assignments, economic changes can be transmitted through rating migrations into average portfolio PD and hence cyclical capital requirements.",
    ["portfolio calibration", "grade calibration", "rating migrations", "cyclical capital requirements"])

add("EBA-08", "How should incomplete recovery processes be treated in LGD estimation according to the approach discussed in the EBA report?",
    ["EBA IRB modelling practices"], "LGD", "hard", True,
    "The approach aligned with the Guidelines includes both recoveries realised up to the estimation point and estimated future recoveries.",
    ["incomplete recovery", "recoveries realised", "estimated future recoveries"])

add("EBA-09", "What were the three most common categories of triggers for additional conservatism in PD model application shown in Table 67?",
    ["EBA IRB modelling practices"], "table", "hard", True,
    "The listed triggers included missing ratings (35% of PD models), missing data in the current portfolio (33%), and outdated ratings in the current portfolio (25%). The question was multiple-select, so percentages need not sum to 100%.",
    ["missing ratings", "35%", "missing data", "33%", "outdated ratings", "25%"])

add("EBA-10", "What does the EBA report say about the frequency of review of estimates?",
    ["EBA IRB modelling practices"], "monitoring", "medium", True,
    "The Guidelines specify an annual review of estimates, supported by a framework with minimum analysis scope, predefined metrics and standards, and predefined actions when deviations occur.",
    ["annual review", "predefined metrics", "predefined standards", "deviations"])

add("EBA-11", "How does the EBA report describe the treatment of accounting provisions in ELBE estimation?",
    ["EBA IRB modelling practices"], "ELBE", "hard", True,
    "The survey found accounting provisions were used for ELBE estimation in 26% of models and exposures; the report notes that the Guidelines would require a change in modelling practices for these models.",
    ["accounting provisions", "ELBE", "26%"])

add("EBA-12", "What limitation does the EBA report explicitly attach to interpreting its survey results?",
    ["EBA IRB modelling practices"], "data_quality", "easy", True,
    "The results depend on the quality of submitted survey responses and are therefore subject to data-quality issues; some respondents also appear not to have understood some questions as intended.",
    ["quality", "submitted responses", "data quality", "questions", "understood"])


# ---------------- Basel: 12 ----------------
add("BAS-01", "For corporate, sovereign and bank exposures under the Basel IRB approach, what does PD represent?",
    ["Basel Framework"], "IRB", "easy", True,
    "PD is the one-year probability of default associated with the internal borrower grade to which the exposure is assigned.",
    ["one-year PD", "internal borrower grade"])

add("BAS-02", "What PD floor does the Basel Framework specify for corporate, sovereign and bank exposures, excluding sovereign exposures?",
    ["Basel Framework"], "IRB", "medium", True,
    "For these exposures, except sovereign exposures, the PD used in the risk-weight formula and expected-loss calculation must not be less than 0.05%.",
    ["0.05%", "PD floor", "corporate", "sovereign", "bank"])

add("BAS-03", "What happens to the PD of borrowers assigned to a default grade under the Basel IRB framework?",
    ["Basel Framework"], "IRB", "medium", True,
    "The PD is 100%, provided the default grade is consistent with the reference definition of default.",
    ["default grade", "100%", "reference definition of default"])

add("BAS-04", "What two approaches can banks use to derive LGD for corporate, sovereign and bank exposures?",
    ["Basel Framework"], "IRB", "easy", True,
    "Banks can use the foundation IRB approach or the advanced IRB approach for deriving LGD.",
    ["LGD", "foundation", "advanced"])

add("BAS-05", "What are PD, LGD, EAD and M used for in the Basel IRB framework?",
    ["Basel Framework"], "IRB", "easy", True,
    "They are the risk components used as inputs to the risk-weight functions for relevant asset classes.",
    ["PD", "LGD", "EAD", "M", "risk-weight functions"])

add("BAS-06", "What information about internal credit-risk models must banks disclose under the Basel Pillar 3 IRB disclosures?",
    ["Basel Framework"], "disclosure", "hard", True,
    "The disclosures include information on model development, controls and changes; independence of model review; reporting; scope of supervisory acceptance; exposure coverage; key models; and characteristics such as PD estimation/validation, LGD and credit conversion factors.",
    ["model development", "controls", "independence", "PD", "LGD", "credit conversion factors"])

add("BAS-07", "What is the purpose of the Basel CR6 disclosure template?",
    ["Basel Framework"], "disclosure", "medium", True,
    "CR6 provides the main parameters used to calculate capital requirements for IRB models and aims to enhance transparency of banks' RWA calculations and the reliability of regulatory measures.",
    ["CR6", "main parameters", "capital requirements", "RWA", "transparency"])

add("BAS-08", "How frequently is the Basel CR6 IRB credit-risk disclosure template reported?",
    ["Basel Framework"], "disclosure", "easy", True,
    "The CR6 template is mandatory for banks using F-IRB or A-IRB for some or all exposures and is reported semiannually.",
    ["CR6", "semiannual"])

add("BAS-09", "What are the three components of the Basel standardised approach capital requirement for market risk?",
    ["Basel Framework"], "market_risk", "medium", True,
    "The capital requirement is the simple sum of the sensitivities-based method requirement, the default risk capital requirement and the residual risk add-on.",
    ["sensitivities-based method", "default risk capital", "residual risk add-on"])

add("BAS-10", "What does the Basel Framework expect banks to do about risk data during stress or crisis situations?",
    ["Basel Framework"], "risk_data", "medium", True,
    "Banks should be able to produce aggregated risk data rapidly during stress or crisis for all critical risks, with frequency requirements capable of producing timely, up-to-date information.",
    ["stress", "crisis", "rapidly", "aggregated risk data", "critical risks"])

add("BAS-11", "What does Basel mean by adaptability in risk data aggregation?",
    ["Basel Framework"], "risk_data", "medium", True,
    "Adaptability means risk data aggregation should be flexible enough to support ad hoc requests and emerging risks, including customisation, incorporation of business or external changes, and regulatory changes.",
    ["adaptability", "ad hoc", "emerging risks", "regulatory framework"])

add("BAS-12", "A bank wants to reduce its leverage-ratio exposure measure by netting collateral received against derivative exposures. Does the Basel Framework permit that?",
    ["Basel Framework"], "leverage_ratio", "hard", True,
    "No. Collateral received may not be netted against derivative exposures for the leverage-ratio exposure measure, even where netting is permitted under accounting or risk-based frameworks.",
    ["collateral received", "not netted", "derivative exposures", "leverage ratio"])


# ---------------- 15 cross-document ----------------
add("X-01", "Compare the role of model validation in PRA SS1/23 and SR 11-7. What common objective do the two documents assign to validation?",
    ["PRA SS1/23", "SR 11-7"], "cross_document", "medium", True,
    "Both treat validation as an independent, critical challenge intended to assess model suitability/soundness and identify limitations or model risk. PRA SS1/23 emphasises objective and unbiased validation; SR 11-7 emphasises conceptual soundness, monitoring and outcomes analysis.",
    ["validation", "objective", "independent", "soundness", "limitations"])

add("X-02", "A bank is building an IRB PD model. Which aspects of model development should it consider under the EBA report, and what broader governance principles would PRA SS1/23 expect around the model lifecycle?",
    ["EBA IRB modelling practices", "PRA SS1/23"], "cross_document", "hard", True,
    "The EBA report discusses risk differentiation, calibration, data representativeness and default definitions for PD development. PRA SS1/23 adds lifecycle governance such as model ownership, tiering, documentation, validation and performance monitoring.",
    ["risk differentiation", "calibration", "data representativeness", "model owner", "tiering", "validation", "monitoring"])

add("X-03", "How do IFRS 9 and the EBA IRB report differ in their treatment of credit-risk measurement objectives?",
    ["IFRS 9", "EBA IRB modelling practices"], "cross_document", "hard", True,
    "IFRS 9 defines expected credit losses as probability-weighted present-value cash shortfalls and focuses on impairment recognition and measurement. The EBA report focuses on IRB regulatory risk-parameter estimation practices such as PD, LGD and ELBE and their calibration/estimation requirements.",
    ["expected credit losses", "cash shortfalls", "PD", "LGD", "ELBE", "calibration"])

add("X-04", "A model validator finds that a credit model performs well statistically but has poorly documented assumptions. How would SR 11-7 and PRA SS1/23 each frame this issue?",
    ["SR 11-7", "PRA SS1/23"], "cross_document", "hard", True,
    "Both documents treat assumptions and conceptual/design soundness as important parts of validation, so strong statistical outcomes do not eliminate the need to understand and document assumptions and limitations.",
    ["assumptions", "conceptual soundness", "validation", "limitations"])

add("X-05", "An IRB model has missing data in the current portfolio. Which document directly discusses additional conservatism for this situation, and what related MRM concept would PRA SS1/23 make relevant?",
    ["EBA IRB modelling practices", "PRA SS1/23"], "cross_document", "hard", True,
    "The EBA report lists missing current-portfolio data as a trigger for additional conservatism in PD-model application. PRA SS1/23 would make data quality, model limitations and performance monitoring relevant to identifying and managing the resulting model risk.",
    ["missing data", "additional conservatism", "data quality", "limitations", "monitoring"])

add("X-06", "A bank modifies a loan and derecognises the original asset. How does IFRS 9's treatment of the modified asset differ conceptually from Basel's use of PD, LGD and EAD in capital calculations?",
    ["IFRS 9", "Basel Framework"], "cross_document", "medium", True,
    "IFRS 9 treats the derecognised-and-replaced asset as a new financial asset for impairment purposes. Basel's IRB framework uses risk components such as PD, LGD and EAD as inputs to regulatory risk-weight calculations; the documents address different measurement frameworks and purposes.",
    ["new financial asset", "impairment", "PD", "LGD", "EAD", "risk-weight"])

add("X-07", "How do the Basel Framework and SR 11-7 both address model/data reliability?",
    ["Basel Framework", "SR 11-7"], "cross_document", "medium", True,
    "SR 11-7 requires assessment of data relevance and model reliability through validation and outcomes analysis. Basel requires risk data aggregation to be accurate, complete, timely and adaptable, with controls and validation of data quality.",
    ["reliability", "data", "validation", "accuracy", "complete", "timely"])

add("X-08", "A vendor supplies a credit-risk model used for regulatory reporting. Which two documents provide directly relevant guidance on how the bank should control this situation?",
    ["SR 11-7", "PRA SS1/23"], "cross_document", "medium", True,
    "SR 11-7 directly addresses validation of vendor models, including limitations, assumptions, benchmarking and contingency planning. PRA SS1/23 provides broader lifecycle governance, ownership, validation and model inventory expectations applicable to the firm's MRM framework.",
    ["vendor", "validation", "benchmarking", "contingency", "model inventory", "ownership"])

add("X-09", "A model's outputs change dramatically after a very small change in an input. Which validation concept in SR 11-7 is most directly relevant, and what PRA lifecycle activity should follow if the weakness is material?",
    ["SR 11-7", "PRA SS1/23"], "cross_document", "medium", True,
    "SR 11-7 identifies sensitivity analysis as a way to detect instability from small input changes. Under PRA SS1/23, the limitation should be identified, monitored, recorded and remediated through the model lifecycle and appropriate validation/governance.",
    ["sensitivity analysis", "unstable", "limitation", "remediated", "validation"])

add("X-10", "What is a common theme between IFRS 9's forward-looking information requirement and the EBA report's concern with representativeness of data?",
    ["IFRS 9", "EBA IRB modelling practices"], "cross_document", "hard", True,
    "Both require model/measurement processes to use information that is relevant to the risk being assessed: IFRS 9 requires reasonable and supportable historical and forward-looking information for credit-risk assessment, while the EBA discusses representativeness of data for risk differentiation and quantification.",
    ["forward-looking", "reasonable and supportable", "representativeness", "risk differentiation", "risk quantification"])

add("X-11", "Which document in the corpus contains survey percentages for current IRB modelling practices, and why should those percentages not be presented as current industry-wide statistics?",
    ["EBA IRB modelling practices"], "cross_document", "medium", True,
    "The EBA report contains survey percentages, but the survey reflects practices at the time of completion in January 2017 and covers a defined sample of institutions and approved models. Therefore the figures should be described with that population and time context.",
    ["January 2017", "survey", "sample", "approved models", "percentages"])

add("X-12", "A RAG answer claims that 'all models must be validated annually.' Which source would you inspect first, and what nuance should the answer preserve?",
    ["SR 11-7", "PRA SS1/23"], "cross_document", "hard", True,
    "SR 11-7 should be inspected first because it explicitly says banks should conduct a periodic review at least annually and material changes should be validated. The answer should not overgeneralise this into an identical annual full-validation requirement for every circumstance; the guidance distinguishes periodic review from the full validation process.",
    ["at least annually", "periodic review", "material changes", "full validation"])

add("X-13", "Which source would you use to answer a question about the minimum PD floor for corporate IRB exposures, and why would the EBA survey report not be the primary source?",
    ["Basel Framework", "EBA IRB modelling practices"], "cross_document", "medium", True,
    "The Basel Framework is the primary source because it states the regulatory PD floor. The EBA report is primarily a survey and impact-assessment document describing modelling practices and policy choices rather than being the corpus's primary statement of the Basel PD floor.",
    ["Basel Framework", "0.05%", "PD floor", "survey"])

add("X-14", "A user asks whether a single on-time payment after a distressed-loan modification proves that credit risk has decreased. Which source contains the most direct answer, and what does it say?",
    ["IFRS 9"], "cross_document", "easy", True,
    "IFRS 9 gives the direct answer: a single timely payment would not typically erase a history of missed or incomplete payments; consistently good payment behaviour over a period is generally needed before credit risk is considered to have decreased.",
    ["single payment", "missed", "consistently good payment behaviour"])

add("X-15", "Which two sources would you combine to evaluate whether a financial model is both technically sound and appropriately governed, and what distinct evidence would each contribute?",
    ["SR 11-7", "PRA SS1/23"], "cross_document", "medium", True,
    "SR 11-7 contributes validation evidence such as conceptual soundness, sensitivity analysis, monitoring, benchmarking and outcomes analysis. PRA SS1/23 contributes lifecycle governance evidence such as model ownership, tiering, inventory, validation independence and performance monitoring.",
    ["conceptual soundness", "sensitivity", "benchmarking", "outcomes", "ownership", "tiering", "inventory"])


# Add 10 unanswerable/negative controls, replacing some overly factual duplicates by design
# These are deliberately plausible but not supported by the five-document corpus.
negatives = [
    ("NEG-01", "What accuracy percentage did the RAG system achieve on the PRA SS1/23 document?", ["PRA SS1/23"]),
    ("NEG-02", "Which of the five documents recommends using FAISS for semantic search?", ["PRA SS1/23","EBA IRB modelling practices","IFRS 9","SR 11-7","Basel Framework"]),
    ("NEG-03", "What was the average F1 score of EBA's IRB models in the survey?", ["EBA IRB modelling practices"]),
    ("NEG-04", "What neural-network architecture does IFRS 9 prescribe for expected credit-loss modelling?", ["IFRS 9"]),
    ("NEG-05", "What embedding model does the Basel Committee recommend for searching the Basel Framework?", ["Basel Framework"]),
    ("NEG-06", "What is the recommended cosine-similarity threshold for retrieving SR 11-7 passages?", ["SR 11-7"]),
    ("NEG-07", "How many tokens should a bank use when chunking model-validation documentation under PRA SS1/23?", ["PRA SS1/23"]),
    ("NEG-08", "What percentage of banks in the EBA survey used transformer-based PD models?", ["EBA IRB modelling practices"]),
    ("NEG-09", "What is the annual API cost assumed by IFRS 9 for generating expected credit-loss forecasts?", ["IFRS 9"]),
    ("NEG-10", "Which of the five documents states that GPT-4 should be used for model validation?", ["PRA SS1/23","EBA IRB modelling practices","IFRS 9","SR 11-7","Basel Framework"])
]

for qid,q,docs in negatives:
    add(qid,q,docs,"unanswerable","hard",False,
        "The corpus does not provide this information. A correct RAG response should explicitly state that the answer cannot be determined from the supplied documents rather than inventing a value or recommendation.",
        ["not in corpus", "cannot be determined", "insufficient evidence"])

# Make exactly 85
assert len(dataset) == 85, len(dataset)
#%%
# Add expected evidence granularity and scoring notes
for row in dataset:
    row["retrieval_target"] = {
        "documents": row["expected_documents"],
        "must_retrieve_evidence": row["evidence_keywords"]
    }
    row["evaluation_notes"] = {
        "retrieval": "Relevant source/chunk(s) should be retrieved.",
        "faithfulness": "Every factual claim in the answer should be supported by retrieved text.",
        "citation": "Citations should point to the source(s) actually supporting the claims.",
        "abstention": "For unanswerable cases, the system should abstain rather than fabricate."
    }

out_json = "data/fin_reg_ai_85_question_evaluation_dataset.json"
out_csv = "data/fin_reg_ai_85_question_evaluation_dataset.csv"

with open(out_json, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

fields = ["id","question","expected_documents","category","difficulty","answerable","reference_answer","evidence_keywords"]
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in dataset:
        w.writerow({k: r[k] for k in fields})
#%%
# Summary
from collections import Counter
summary = {
    "total": len(dataset),
    "by_document": Counter(d for r in dataset for d in r["expected_documents"]),
    "by_category": Counter(r["category"] for r in dataset),
    "by_difficulty": Counter(r["difficulty"] for r in dataset),
    "answerable": sum(r["answerable"] for r in dataset),
    "unanswerable": sum(not r["answerable"] for r in dataset),
}
print("Created:", out_json)
print("Created:", out_csv)
print("Total questions:", summary["total"])
print("Answerable:", summary["answerable"], "| Unanswerable:", summary["unanswerable"])
print("Categories:", dict(summary["by_category"]))
print("Difficulty:", dict(summary["by_difficulty"]))
#%%
# The previous construction succeeded up to the final assertion; reduce it to the intended 75:
# 50 answerable single-document + 10 unanswerable controls + 15 cross-document.
remove_ids = {"PRA-11","PRA-12","SR-11","SR-12","IFRS-11","IFRS-12",
              "EBA-11","EBA-12","BAS-11","BAS-12"}
dataset = [r for r in dataset if r["id"] not in remove_ids]

# The 10 negative controls were already appended in the prior construction.
assert len(dataset) == 75, len(dataset)
#%%
for row in dataset:
    row["retrieval_target"] = {
        "documents": row["expected_documents"],
        "must_retrieve_evidence": row["evidence_keywords"]
    }
    row["evaluation_notes"] = {
        "retrieval": "Relevant source/chunk(s) should be retrieved.",
        "faithfulness": "Every factual claim in the answer should be supported by retrieved text.",
        "citation": "Citations should point to the source(s) actually supporting the claims.",
        "abstention": "For unanswerable cases, the system should abstain rather than fabricate."
    }

out_json = "data/fin_reg_ai_75_question_evaluation_dataset.json"
out_csv = "data/fin_reg_ai_75_question_evaluation_dataset.csv"

with open(out_json, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

fields = ["id","question","expected_documents","category","difficulty","answerable","reference_answer","evidence_keywords"]
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in dataset:
        w.writerow({k: r[k] for k in fields})

from collections import Counter
by_doc = Counter()
for r in dataset:
    for d in r["expected_documents"]:
        by_doc[d] += 1

print("Created:", out_json)
print("Created:", out_csv)
print("Total:", len(dataset))
print("Answerable:", sum(r["answerable"] for r in dataset))
print("Unanswerable:", sum(not r["answerable"] for r in dataset))
print("Single-document:", sum(len(r["expected_documents"]) == 1 for r in dataset))
print("Cross-document:", sum(len(r["expected_documents"]) > 1 for r in dataset))
print("Difficulty:", dict(Counter(r["difficulty"] for r in dataset)))