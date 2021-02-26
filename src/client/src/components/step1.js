import { Row, Col, Form, Button } from 'react-bootstrap';
import RadioButton from './common/radioButton';

const Step1 = ({ src_lang, tgt_lang, setForm, formData, navigation, handleSubmitFeedback }) => {

    const { know_language1, know_language2 } = formData;
    
    const { next, go } = navigation;

    const handleNext= () => {
        if(know_language1 === "none" && know_language2 === "none") {
            // submit feedback
            handleSubmitFeedback();
            // then skip next step
            go("step3");
        } else {
            // go to next page
            next();
        }
    }

    return (
        <div>
            <div style={{textAlign: 'center'}}>
                <h6 style={{ fontSize: 13, color: 'gray' }}>Part 1/2</h6>
            </div>

            <div style={{textAlign: 'center'}}>
                <p style={{ fontSize: 13, fontWeight: 'bold' }}>How well do you know {src_lang}?</p>
                <Form>
                    <Row>
                        <Col>
                            <RadioButton 
                                value="none"
                                name="know_language1"
                                label="Not at all"
                                selected={know_language1}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="little"
                                name="know_language1" 
                                label="A little bit"
                                selected={know_language1}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="decent"
                                name="know_language1" 
                                label="A decent amount"
                                selected={know_language1}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="well"
                                name="know_language1" 
                                label="Very well"
                                selected={know_language1}
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
                <p style={{ fontSize: 13, fontWeight: 'bold' }}>How well do you know {src_lang}?</p>
                <Form>
                    <Row>
                        <Col>
                            <RadioButton 
                                value="none"
                                name="know_language2"
                                label="Not at all"
                                selected={know_language2}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="little"
                                name="know_language2" 
                                label="A little bit"
                                selected={know_language2}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="decent"
                                name="know_language2" 
                                label="A decent amount"
                                selected={know_language2}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="well"
                                name="know_language2" 
                                label="Very well"
                                selected={know_language2}
                                onChange={setForm} 
                            />
                        </Col>
                    </Row>
                </Form>
            </div>

            <br />
            <hr />
            <br />

            <div style={{textAlign: "right"}}>
                <Button size="sm" variant="outline-primary" onClick={handleNext}>NEXT</Button>
            </div>
        </div>
    )
}

export default Step1;
