import c from './CEditButton.module.css';
import {clsx} from "clsx";

export default function CEditButton({buttonName, onClick}) {
	
	return (
		<span className={clsx(c.editButton, "cursor-pointer")} onClick={() => onClick?.()}>
      {buttonName}
    </span>
	)
	
}