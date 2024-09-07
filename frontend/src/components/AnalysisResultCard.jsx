/* eslint-disable react/prop-types */
const AnalysisResultCard = ({ result }) => {
  const {
    procedure_overview,
    observations,
    identification,
    procedural_steps,
    surgical_technique,
    critical_moments,
    clinical_significance,
    educational_summary
  } = JSON.parse(result.analysis_result);

  const renderList = (items) => (
    <ul className="list-disc list-inside">
      {items.map((item, index) => (
        <li key={index} className="mb-2">{item}</li>
      ))}
    </ul>
  );

  const renderSection = (title, content) => (
    <div className="collapse collapse-arrow bg-base-200 mb-4">
      <input type="checkbox" /> 
      <div className="collapse-title text-xl font-medium">
        {title}
      </div>
      <div className="collapse-content"> 
        {typeof content === 'string' ? <p>{content}</p> : renderList(content)}
      </div>
    </div>
  );

  return (
    <div className="card bg-base-100 shadow-xl">
      <div className="card-body">
        <h2 className="card-title text-2xl font-bold mb-4">Analysis Results</h2>
        
        {renderSection("Procedure Overview", procedure_overview)}
        {renderSection("Observations", observations)}
        
        <div className="collapse collapse-arrow bg-base-200 mb-4">
          <input type="checkbox" /> 
          <div className="collapse-title text-xl font-medium">
            Identification
          </div>
          <div className="collapse-content"> 
            {renderSection("Structures", identification.structures)}
            {renderSection("Instruments", identification.instruments)}
            {renderSection("Uncertainties", identification.uncertainties)}
          </div>
        </div>
        
        {renderSection("Procedural Steps", procedural_steps)}
        {renderSection("Surgical Technique", surgical_technique)}
        {renderSection("Critical Moments", critical_moments)}
        {renderSection("Clinical Significance", clinical_significance)}
        {renderSection("Educational Summary", educational_summary)}
        
        <div className="card-actions justify-end mt-4">
          <a 
            href={result.output_video_path} 
            target="_blank" 
            rel="noopener noreferrer" 
            className="btn btn-primary"
          >
            View Analyzed Video
          </a>
        </div>
      </div>
    </div>
  );
};

export default AnalysisResultCard;