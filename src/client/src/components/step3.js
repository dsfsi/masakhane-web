import { Button } from 'react-bootstrap';

const Step3 = ({ setShow }) => {
    const handleShow = () => setShow(false);

    return (
        <div style={{textAlign: 'center'}}>
            <h6>THANK YOU!</h6>
            {/* <p style={{fontSize: 11, color: 'gray'}}>We appreciate your feedback and your contribution which help us make translations better.</p> */}
            <div>
                <Button size="sm" variant="outline-primary" onClick={handleShow}>Done</Button>
            </div>
        </div>
    )
}

export default Step3;
