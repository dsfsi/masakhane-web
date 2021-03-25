import { Row, Col, Form, Button } from 'react-bootstrap';
import RadioButton from './common/radioButton';

const Step1 = ({ src_lang, tgt_lang, setForm, formData, navigation, handleSubmitFeedback }) => {

    const { know_src_lang, know_tgt_lang } = formData;
    
    const { next, go } = navigation;

    const handleNext= () => {
        if(know_src_lang === "none" && know_tgt_lang === "none") {
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
                                name="know_src_lang"
                                label="Not at all"
                                selected={know_src_lang}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="little"
                                name="know_src_lang" 
                                label="A little bit"
                                selected={know_src_lang}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="decent"
                                name="know_src_lang" 
                                label="A decent amount"
                                selected={know_src_lang}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="well"
                                name="know_src_lang" 
                                label="Very well"
                                selected={know_src_lang}
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
                <p style={{ fontSize: 13, fontWeight: 'bold' }}>How well do you know {tgt_lang}?</p>
                <Form>
                    <Row>
                        <Col>
                            <RadioButton 
                                value="none"
                                name="know_tgt_lang"
                                label="Not at all"
                                selected={know_tgt_lang}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="little"
                                name="know_tgt_lang" 
                                label="A little bit"
                                selected={know_tgt_lang}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="decent"
                                name="know_tgt_lang" 
                                label="A decent amount"
                                selected={know_tgt_lang}
                                onChange={setForm} 
                            />
                        </Col>
                        <Col>
                            <RadioButton 
                                value="well"
                                name="know_tgt_lang" 
                                label="Very well"
                                selected={know_tgt_lang}
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
