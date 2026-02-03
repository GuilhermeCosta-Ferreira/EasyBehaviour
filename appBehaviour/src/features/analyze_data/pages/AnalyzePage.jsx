import Button from "../../../shared/ui/Button/Button";
import SectionTitle from "../../../shared/ui/SectionTitle/SectionTitle";
import { useNavigate } from "react-router-dom";
import TestPlot from "../components/TestPlot/TestPlot";
import SelectionMenu from "../components/SelectionMenu/SelectionMenu";

function AnalysePage() {
  const navigate = useNavigate();

  return (
    <div>
      <SectionTitle>Analyze Data</SectionTitle>
      <SelectionMenu></SelectionMenu>
      <TestPlot></TestPlot>
      <Button className="container" onClick={() => navigate("/")}>Go Back</Button>
    </div>
  )
}

export default AnalysePage
