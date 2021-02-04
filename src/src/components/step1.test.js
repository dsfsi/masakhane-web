import { render, screen } from '@testing-library/react';
import Step1 from './step1';

describe('Step1', () => {
  test('renders Step1 component', () => {
    const props = { 
      language1: "none", 
      language2: "none", 
      setForm: () => {}, 
      formData: {}, 
      navigation: {}, 
      handleSubmitFeedback: () => {} 
    };
    render(<Step1 {...props} />);
  });
});
