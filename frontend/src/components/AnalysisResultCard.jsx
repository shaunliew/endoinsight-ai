/* eslint-disable react/prop-types */
import { ChevronRight, ChevronDown } from 'lucide-react';
import ReactPlayer from 'react-player'

function AnalysisResultCard({ result }) {
  if (!result || !result.analysis_result) {
    return null;
  }

  const analysisData = JSON.parse(result.analysis_result);

  function renderList(items) {
    return (
      <ul className="space-y-2">
        {items.map((item, index) => (
          <li key={index} className="flex items-start">
            <span className="inline-block w-6 h-6 rounded-full bg-primary text-white text-center leading-6 mr-2 flex-shrink-0">
              {index + 1}
            </span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    );
  }

  function renderSteps(steps) {
    return (
      <ul className="steps steps-vertical">
        {steps.map((step, index) => (
          <li key={index} className="step step-primary">{step}</li>
        ))}
      </ul>
    );
  }

  function renderSection(title, content) {
    return (
      <div className="collapse collapse-plus bg-base-100 mb-4 border rounded-box hover:shadow-md transition-shadow duration-300">
        <input type="checkbox" className="peer" /> 
        <div className="collapse-title text-xl font-medium flex items-center peer-checked:bg-base-200">
          <ChevronRight className="mr-2 peer-checked:hidden" />
          <ChevronDown className="mr-2 hidden peer-checked:inline" />
          {title}
        </div>
        <div className="collapse-content bg-base-100"> 
          <div className="mt-2">
            {title === "Procedural Steps" ? renderSteps(content) : 
             (typeof content === 'string' ? <p>{content}</p> : renderList(content))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card bg-base-100 border shadow-xl">
      <div className="card-body">
        <h2 className="card-title text-3xl font-bold mb-6">Analysis Results</h2>
        
        {renderSection("Procedure Overview", analysisData.procedure_overview)}
        {renderSection("Observations", analysisData.observations)}
        
        <div className="collapse collapse-plus bg-base-100 mb-4 border rounded-box hover:shadow-md transition-shadow duration-300">
          <input type="checkbox" className="peer" /> 
          <div className="collapse-title text-xl font-medium flex items-center peer-checked:bg-base-200">
            <ChevronRight className="mr-2 peer-checked:hidden" />
            <ChevronDown className="mr-2 hidden peer-checked:inline" />
            Identification
          </div>
          <div className="collapse-content bg-base-100"> 
            <div className="mt-2">
              {renderSection("Structures", analysisData.identification.structures)}
              {renderSection("Instruments", analysisData.identification.instruments)}
              {renderSection("Uncertainties", analysisData.identification.uncertainties)}
            </div>
          </div>
        </div>
        
        {renderSection("Procedural Steps", analysisData.procedural_steps)}
        {renderSection("Surgical Technique", analysisData.surgical_technique)}
        {renderSection("Critical Moments", analysisData.critical_moments)}
        {renderSection("Clinical Significance", analysisData.clinical_significance)}
        {renderSection("Educational Summary", analysisData.educational_summary)}
        
        <div className="mt-6">
          <h3 className="text-xl font-semibold mb-2">Analyzed Video</h3>
          <div className="relative w-full" style={{ paddingTop: '56.25%' }}> {/* 16:9 Aspect Ratio */}
            <ReactPlayer
              url={result.output_video_url}
              controls
              width="100%"
              height="100%"
              style={{ position: 'absolute', top: 0, left: 0 }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default AnalysisResultCard;