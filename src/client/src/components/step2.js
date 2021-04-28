import { Row, Col, Form, Button } from 'react-bootstrap';
import RadioButton from './common/radioButton';
import React from 'react';

const Step2 = ({ src_lang, tgt_lang, text, translation, setForm, formData, navigation, handleSubmitFeedback }) => {

    const { understand_translation, accurate_translation, own_translation } = formData;
    const { next } = navigation;

    const handleSubmit = () => {
        // submit form
        handleSubmitFeedback();
        // then navigate to next page
        next();
    }
    return (
        <div>
            <div style={{textAlign: 'center'}}>
                <h6 style={{ fontSize: 13, color: 'gray' }}>Part 2/2</h6>
            </div>

            <div style={{textAlign: 'center'}}>
                <Row>
                    <Col>
                        <p style={{ color: 'gray', fontSize: 11 }}>{!!src_lang && src_lang.toUpperCase()}</p>
                        <p style={{ fontSize: 11 }}>{text}</p>
                    </Col>
                    <Col><i className="fa fa-arrow-right"></i></Col>
                    <Col>
                        <p style={{ color: 'gray', fontSize: 11 }}>{!!tgt_lang && tgt_lang.toUpperCase()}</p>
                        <p style={{ fontSize: 11 }}>{!!translation && translation}</p>
                    </Col>
                </Row>
            </div>

            <br />
            <hr />
            <br />

            <div style={{textAlign: 'center'}}>
                <p style={{ fontSize: 13, fontWeight: 'bold' }}>Did you understand the translation? / Did it make sense?</p>
                <Form>
                    <Row>
                        <Col>
                            <RadioButton 
                                value="none"
                                name="understand_translation"
                                label="Not at all"
                                selected={understand_translation}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="some"
                                name="understand_translation"
                                label="Some of it"
                                selected={understand_translation}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="most"
                                name="understand_translation"
                                label="Most of it"
                                selected={understand_translation}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="absolutely"
                                name="understand_translation"
                                label="Absolutely"
                                selected={understand_translation}
                                onChange={setForm} 
                            />
                        </Col>
                    </Row>
                </Form>
            </div>

            <br />
            <hr />
            <br />

            <div style={{textAlign: 'center'}}>
                <p style={{ fontSize: 13, fontWeight: 'bold' }}>How accurate was the translation?</p>
                <Form>
                    <Row>
                        <Col>
                            <RadioButton 
                                value="nonsense"
                                name="accurate_translation"
                                label="Nonsense"
                                selected={accurate_translation}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="needs_work"
                                name="accurate_translation"
                                label="Needs alot of work"
                                selected={accurate_translation}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="needs_tweaking"
                                name="accurate_translation"
                                label="Needs tweaking"
                                selected={accurate_translation}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="accurate"
                                name="accurate_translation"
                                label="Accurate"
                                selected={accurate_translation}
                                onChange={setForm} 
                            />
                        </Col>
                    </Row>
                </Form>
            </div>

            <br />
            <hr />
            <br />

            <div style={{textAlign: 'center'}}>
                <p style={{ fontSize: 13, fontWeight: 'bold' }}>How would you have translated this? (Optional)</p>
                <div style={{width: '100%', margin: '0 auto', borderWidth: 1, borderColor: 'gray' }}>
                    <Form>
                        <Form.Group controlId="Form.ControlTextarea2">
                            <Form.Control 
                                as="textarea"
                                placeholder="Enter your translation here..." 
                                rows="3" 
                                name="own_translation"
                                style={{ height: '100px', fontSize: 13 }} 
                                value={own_translation}
                                onChange={setForm}
                            />
                        </Form.Group>
                    </Form>
                </div>
            </div>

            <br />
            <hr />
            <br />

            <div style={{textAlign: "right"}}>
                <Button size="sm" variant="outline-primary" onClick={handleSubmit}>SUBMIT</Button>
            </div>
        </div>
    )
}

export default Step2;
