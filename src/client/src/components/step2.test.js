import { render, screen } from '@testing-library/react';
import Step2 from './step2';

describe('Step2', () => {
  test('renders Step2 component', () => {
    const props = { 
      src_lang: "none", 
      tgt_lang: "none",
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