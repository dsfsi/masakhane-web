import { useState } from 'react';
import { Row, Card, Button } from 'react-bootstrap';

const Terms = ({ setShow, navigation }) => {

    const [acceptedTerms, setAcceptedTerms] = useState(false);
    
    const { next } = navigation;

    const handleAccept = () => {
        setAcceptedTerms(true);
        // TODO: record time when user accepted terms

        // proceed
        next();
    }

    const handleDecline = () => {
        setAcceptedTerms(false);
        // close modal
        setShow(false);
    }

    return (
        <div>
            <Card style={{ width: '100%' }}>
                <Card.Body>
                    <Card.Title>Consent Letter</Card.Title>
                    <Card.Subtitle className="mb-2 text-muted">Dear Sir/Madam,</Card.Subtitle>
                    <div>
                        <Card.Text style={{ fontSize: 12, color: 'gray' }}>
                            I am <span><b>Dr Vukosi Marivate</b></span>, principal investigator of the Data Science for Social Impact research group at the Department of Computer Science at the University of Pretoria. 
                            The research project is titled <span><b>Masakhane Web Feedback Analysis for African Language Task Models</b></span>. 
                            The study aims to understand the challenges in automated translation models for African languages. 
                            The models themselves are sourced from the Masakhane project (our collaborators) and are all a work in progress. By better providing feedback to model designers, we can work to improve the models and conduct research on African Language Natural Language Processing. 
                            The purpose of this questionnaire/feedback form is to collect information on the quality of the translations that are on the Masakhane Web system currently. 
                            The user participation is voluntary, and you can withdraw at any time without penalty. 
                        </Card.Text>
                    </div>
                    <br />
                    <div>
                        <Card.Text style={{ fontSize: 12, color: 'gray' }}>
                            Throughout the feedback from the participants, their privacy remains confidential. 
                            Hence, we only collect the following information:
                            <Card.Text style={{ fontSize: 12, color: 'black' }}>
                                1. The user has the option to accept or reject to participate in the feedback survey,
                            </Card.Text>
                            <Card.Text style={{ fontSize: 12, color: 'black' }}>
                                2. The participants are required to indicate their level of proficiencies of the languages translated by the model, 
                            </Card.Text>
                            <Card.Text style={{ fontSize: 12, color: 'black' }}>
                                3. and your submitted feedback to the translations is stored on our server. No personal information is collected.
                            </Card.Text>
                        </Card.Text>
                    </div>
                    <br />
                    <div>
                        <Card.Text style={{ fontSize: 12, color: 'gray' }}>
                            If you agree to participate, please complete the survey that follows this cover letter. 
                            It should take about 5 minutes of your time at the most for feedback on each translation. 
                            By completing the survey, you indicate your willingness to participate in this research.

                            If you have any concerns, please contact me with the details provided below.
                            <br />
                            <span><b>Dr. Vukosi Marivate</b></span>
                            <br />
                            <span><i>vukosi.marivate@cs.up.ac.za</i></span>
                        </Card.Text>
                    </div>
                </Card.Body>
            </Card>
            <Row style={{ padding: 20, justifyContent: 'space-between'}}>
                <div>
                    <Button size="sm" variant="outline-secondary" onClick={handleDecline}>NOT NOW</Button>
                </div>
                <div>
                    <Button size="sm" variant="outline-primary" onClick={handleAccept}>ACCEPT TERMS</Button>
                </div>
            </Row>
        </div>
    )
}

export default Terms;
