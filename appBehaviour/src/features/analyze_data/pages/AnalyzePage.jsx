import { useNavigate } from "react-router-dom";
import { useCallback, useEffect, useState } from "react";

import Button from "../../../shared/ui/Button/Button";
import SectionTitle from "../../../shared/ui/SectionTitle/SectionTitle";

import SelectionMenu from "../components/SelectionMenu/SelectionMenu";
import CostumPlot from "../components/CostumPlot/CostumPlot";

function AnalysePage() {
  // 1. Initializes the navigate process
  const navigate = useNavigate();

  // 2. Initializes a filter option
  const [selection, setSelection] = useState({});
  const handleChange = useCallback((name, value) => {
      setSelection(prev => {
        // optional: skip if identical reference (helps if you pass same array)
        if (prev[name] === value) return prev;
        return { ...prev, [name]: value };
      });
    }, []);

    useEffect(() => {
      console.log(selection);
    }, [selection]);


  //console.log(selection)

    return (
      <div>
        <SectionTitle>Analyze Data</SectionTitle>
        <SelectionMenu filterCall={handleChange} />
        <CostumPlot filters={selection}></CostumPlot>
        <Button className="container" onClick={() => navigate("/")}>Go Back</Button>
      </div>
    )
  }

export default AnalysePage
