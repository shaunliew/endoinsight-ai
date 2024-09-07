/* eslint-disable react/prop-types */
const TimelineItem = ({ step, event }) => (
    <li>
      <hr />
      <div className="timeline-start timeline-box">{step}</div>
      <div className="timeline-middle">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 20 20"
          fill="currentColor"
          className="h-5 w-5">
          <path
            fillRule="evenodd"
            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z"
            clipRule="evenodd" />
        </svg>
      </div>
      <div className="timeline-end timeline-box">{event}</div>
      <hr />
    </li>
  );
  
  const Timeline = () => {
        const timelineData = [
        { step: "Step 1", event: "Upload endoscopic surgery video for frame extraction using OpenCV" },
        { step: "Step 2", event: "Perform YOLOv8 object segmentation on extracted frames" },
        { step: "Step 3", event: "Extract visual features from YOLOv8 segmentation results" },
        { step: "Step 4", event: "Generate textual explanations using Claude 3 Haiku via Amazon Bedrock" },
        { step: "Step 5", event: "Integrate visual and textual data for comprehensive analysis output" }
      ];
  
    return (
      <div className="flex justify-center w-full">
        <ul className="timeline timeline-vertical">
          {timelineData.map((item, index) => (
            <TimelineItem key={index} step={item.step} event={item.event} />
          ))}
        </ul>
      </div>
    );
  };
  
  export default Timeline;