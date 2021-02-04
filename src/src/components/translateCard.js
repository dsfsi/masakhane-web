import { useState, useRef } from 'react';
import { Container, Row, Col, Form, Button, Modal, Toast, OverlayTrigger, Tooltip } from 'react-bootstrap';
import {CopyToClipboard} from 'react-copy-to-clipboard';

import MultiStepForm from './multiStepForm';

const languages = [
    { id: 1, name: "English" },
    { id: 2, name: "Swahili" },
    { id: 3, name: "Sesotho" },
    { id: 4, name: "Yoruba" },
    { id: 5, name: "Twi" },
];

export default function TranslateCard() {
    const [text, setText] = useState("");
    const [translation, setTranslation] = useState("Translation");
    const [show, setShow] = useState(false);
    const [language1, setLanguage1] = useState('English');
    const [language2, setLanguage2] = useState('Swahili');
    const [feedBackForm, setFeedBackForm] = useState({});

    const textAreaRef = useRef(null);
    const [copySuccess, setCopySuccess] = useState('');
    const [showToast, setShowToast] = useState('');

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const copyToClipboard = () => {
        setCopySuccess('Translation Copied!');
        setShowToast(true);
    };

    const handleChangeLanguage1 = (e) => {
        setLanguage1(e.target.value);
    };

    const handleChangeLanguage2 = (e) => {
        setLanguage2(e.target.value);
    };

    const handleTranslate = () => {
        setTranslation('Translated text test...');
    };

    const submitFeedBack = (formData) => {
        // first set state of feedback Form
        setFeedBackForm({...formData});
        // then submit feedback form to db here
        // here's where you write the function to push feedback to backend

    }

    return (
        <Container className="border">
            <style type="text/css">
                {`
                .header {
                    background-color: aliceblue;
                    height: 60px;
                    font-size: 1rem;
                    padding: 1rem 1.5rem;
                }
                .form-control {
                    border: 0;
                }
                .h-list {
                    border: 0;
                }
                .body {
                    min-height: 250px;
                }
                .text-area {
                    padding-top: 20px;
                    padding-bottom: 20px;
                }
                .translated {
                    font-size: 1.5rem;
                    color: #797979;
                    font-weight: normal;

                }
                .feedback-button {
                    bottom: 10px;
                }
                `}
            </style>

            <Modal show={show} onHide={handleClose} centered>
                <Modal.Header closeButton>
                {/*<Modal.Title>Modal heading</Modal.Title>*/}
                <Col style={{textAlign: 'center'}}>
                    <h4 style={{ fontSize: 14, color: '#717171' }}>GIVE FEEDBACK</h4>
                    <p style={{ fontSize: 11, color: 'gray' }}>We appreciate your feedback and your contribution will help make our translation better.</p>
                </Col>
                </Modal.Header>
                <Modal.Body>
                    <MultiStepForm 
                        language1={language1} 
                        language2={language2} 
                        text={text} 
                        translation={translation} 
                        setShow={setShow}
                        submitFeedBack={submitFeedBack}
                    />
                </Modal.Body>
            </Modal>

            <Row className="header">
                <Col className="border-right">
                    <Row>
                        <Col>
                            <Form inline>
                                <Form.Group controlId="fromform">
                                <Form.Label>From: </Form.Label>
                                    <Form.Control value={language1} className="form-control" as="select" size="md" custom onChange={handleChangeLanguage1}>
                                    {
                                        languages.map((option, index) => {
                                        return (<option key={index} value={option.name}>{option.name}</option>)
                                        })
                                    }
                                    </Form.Control>
                                </Form.Group>
                            </Form>
                        </Col>
                        <Col>
                             <Row>
                            {
                                languages
                                .filter(x => x.name !== language1)
                                .slice(0, 3)
                                .map((option, index) => {
                                return (
                                    <Button key={option.id} variant="light" size="sm" onClick={() => setLanguage1(option.name)}>{option.name}</Button>                                   )
                                })
                            }
                            </Row>
                        </Col>
                    </Row>
                </Col>
                <Col className="ml-3">
                <Row>
                    <Col>
                        <Form inline>
                            <Form.Group controlId="fromform">
                            <Form.Label>To: </Form.Label>
                                <Form.Control value={language2} className="form-control" as="select" size="md" custom onChange={handleChangeLanguage2}>
                                {
                                    languages.map((option, index) => {
                                    return (<option key={option.id} key={index} value={option.name}>{option.name}</option>)
                                    })
                                }
                                </Form.Control>
                            </Form.Group>
                        </Form>
                    </Col>
                    <Col>
                        <Row>
                        {
                            languages
                            .filter(x => x.name !== language2)
                            .slice(0, 3)
                            .map((option, index) => {
                            return (
                                <Button key={option.id} variant="light" size="sm" onClick={() => setLanguage2(option.name)}>{option.name}</Button>                                   )
                            })
                        }
                        </Row>
                    </Col>
                </Row>
                </Col>
            </Row>
            <Row className="body">
                <Col className="border-right text-area">
                    <Form>
                        <Form.Group controlId="Form.ControlTextarea">
                            <Form.Control 
                                as="textarea"
                                placeholder="Enter Text" 
                                rows="3" 
                                name="text"
                                style={{ height: '200px', fontSize: 24 }} 
                                value={text}
                                onChange={e => setText(e.target.value)}
                            />
                        </Form.Group>
                    </Form>
                    
                    <Row>
                        <Col>
                            <Button variant="outline-primary" onClick={handleTranslate}>Translate</Button>
                        </Col>
                        <Col md="auto">{' '}</Col>
                        <Col xs lg="2">
                            <Button variant="outline-danger" size="sm" onClick={() => setText("")}><i className="fas fa-times"></i></Button>{' '}
                        </Col>
                    </Row>
                </Col>
                <Col className="ml-3 text-area">
                    <Form>
                        <Form.Group controlId="Form.ControlTextarea2">
                            <Form.Control 
                                as="textarea"
                                ref={textAreaRef}
                                placeholder="Enter Text" 
                                rows="3" 
                                name="text"
                                style={{ height: '200px', fontSize: 24 }} 
                                value={translation}
                                onChange={e => setText(e.target.value)}
                                autoFocus={showToast}
                            />
                        </Form.Group>
                    </Form>
                    
                    <Row>
                        <Col>
                            <Button variant="light" className="feedback-button" onClick={handleShow}>Give Feedback</Button>
                        </Col>
                        <Col md="auto">{' '}</Col>
                        <Col xs lg="2">
                            <CopyToClipboard text={translation} onCopy={copyToClipboard}>
                                <Button variant="outline-success" size="sm"><i className="fa fa-copy"></i></Button>
                            </CopyToClipboard>
                        </Col>
                    </Row>
                </Col>
            </Row>

            <div aria-live="polite" aria-atomic="true" style={{ position: 'relative' }}>
                <Toast
                    onClose={() => setShowToast(false)} 
                    show={showToast} 
                    delay={3000} 
                    autohide
                    style={{
                        position: 'absolute',
                        bottom: 0,
                        left: 0
                    }}
                >
                    <Toast.Body style={{color: 'green'}}>{copySuccess}</Toast.Body>
                </Toast>
            </div>
        </Container>
    )
}