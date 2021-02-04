import { render, screen } from '@testing-library/react';
import Step2 from './step2';

describe('Step2', () => {
  test('renders Step2 component', () => {
    const props = { 
      language1: "none", 
      language2: "none",
      text: "", 
      translation: "", 
      setForm: () => {}, 
      formData: {}, 
      navigation: {}, 
      handleSubmitFeedback: () => {} 
    };
    render(<Step2 {...props} />);
  });
});