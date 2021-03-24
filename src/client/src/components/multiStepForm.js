import { useForm, useStep } from "react-hooks-helper";

import Terms from "./terms";
import Step1 from "./step1";
import Step2 from "./step2";
import Step3 from "./step3";

const steps = [
    { id: "terms" },
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

const MultiStepForm = ({ src_lang, tgt_lang, text, translation, setShow, submitFeedBack, setFeedbackToken, feedbackToken}) => {
    const [formData, setForm] = useForm({...defaultData, src_lang, tgt_lang, text, translation, feedbackToken});
    const { step, navigation } = useStep({ initialStep: 0, steps });
    const { id } = step;

    const handleSubmitFeedback = () => {
        // set formData to be feedback form
        console.log({formData})
        submitFeedBack(formData);
    }

    const props = { src_lang, tgt_lang, text, translation, setShow, formData, setForm, navigation, handleSubmitFeedback, setFeedbackToken, feedbackToken};

    switch (id) {
        case "terms":
            return <Terms {...props} />;
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
