import clsx from 'clsx';
import s from './CButton.module.css';

export default function CButton({
	path,
	width,
	buttonName,
	onClick,
	type = 'type1',
	beforeIcon,
	afterIcon,
	fontSize,
	padding,
}) {
	const getTypeClass = () => {
		switch (type) {
			case 'type1':
				return s.type1;
			case 'type2':
				return s.type2;
			case 'type3':
				return s.type3;
		}
	};
	return (
		<button
			onClick={() => onClick?.()}
			className={clsx(s.commonButton, getTypeClass(), 'cursor-pointer')}
			style={{
				width: width ? `${width}px` : 'auto',
				fontSize: `${fontSize || 13}px`,
				...(padding && { padding: padding }),
			}}
		>
			{/*<img src={path} alt="" />*/}
			{beforeIcon}
			{buttonName}
			{afterIcon}
		</button>
	);
}
