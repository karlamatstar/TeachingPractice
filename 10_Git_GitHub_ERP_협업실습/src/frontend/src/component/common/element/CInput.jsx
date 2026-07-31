import s from './CInput.module.css'
import {clsx} from "clsx";

export default function CInput({
																 placeholder,
																 width,
																 readOnly = false,
																 disabled = false,
																 value = "",
																 onChange,
																 onKeyDown
															 }) {
	return (
		<>
			<input
				readOnly={readOnly}
				className={clsx(s.cInput, "leading-[15.6px]", readOnly ? s.cInputReadonly : "")}
				style={{width: `${width ?? 120}px`}}
				onChange={e => onChange?.(e)}
				type="text"
				placeholder={placeholder}
				value={value}
				disabled={disabled}
				onKeyDown={e => onKeyDown?.(e)}
			/>
		</>
	)
}