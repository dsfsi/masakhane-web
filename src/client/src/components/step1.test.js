import { render, screen } from '@testing-library/react';
import Step1 from './step1';

describe('Step1', () => {
  test('renders Step1 component', () => {
    const props = { 
      src_lang: "none", 
      tgt_lang: "none", 
      setForm: () => {}, 
      formData: {}, 
      navigation: {}, 
      handleSubmitFeedback: () => {} 
    };
    render(<Step1 {...props} />);
  });
});
