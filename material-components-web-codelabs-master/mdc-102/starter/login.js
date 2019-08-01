import {MDCRipple} from '@material/ripple';
import {MDCTextField} from '@material/textfield';

const email = new MDCTextField(document.querySelector('.email'));
const password = new MDCTextField(document.querySelector('.password'));

new MDCRipple(document.querySelector('.cancel'));
new MDCRipple(document.querySelector('.next'));
