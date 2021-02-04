import { useForm, useStep } from "react-hooks-helper";

import Step1 from "./step1";
import Step2 from "./step2";
import Step3 from "./step3";

const steps = [
    { id: "step1" },
    { id: "step2" },
    { id: "step3" },
];

const defaultData = {
    know_language1: "little",
    know_language2: "little",
    understand_translation: "none",
    accurate_translation: "nonsense",
    own_translation: "",
};

const MultiStepForm = ({ language1, language2, text, translation, setShow, submitFeedBack}) => {
    const [formData, setForm] = useForm(defaultData);
    const { step, navigation } = useStep({ initialStep: 0, steps });
    const { id } = step;

    const handleSubmitFeedback = () => {
        // set formData to be feedback form
        submitFeedBack(formData);
    }

    const props = { language1, language2, text, translation, setShow, formData, setForm, navigation, handleSubmitFeedback };

    switch (id) {
        case "step1":
            return <Step1 {...props} />;
        case "step2":
            return <Step2 {...props} />;
        case "step3":
            return <Step3 {...props} />;

        default:
            return null;
    }
}

export default MultiStepForm;
