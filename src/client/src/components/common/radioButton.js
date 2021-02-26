import { Form } from 'react-bootstrap';

const RadioButton = ({ value, label, selected, ...otherProps }) => {
    return(
        <div>
            <Form.Label style={{ color: 'gray', fontSize: 14 }}>{label}</Form.Label>
            <Form.Check id="none" value={value} type="radio" defaultChecked={selected === value ? true : false} {...otherProps} />
        </div>
    );
}

export default RadioButton;