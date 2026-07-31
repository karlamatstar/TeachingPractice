import s from './CSelect.module.css';
import {useState} from "react";


const departmentList = [
	"전체",
	"경영지원본부",
	"인사팀",
	"재무회계팀",
	"총무팀",
	"물류운영본부",
	"배차팀",
	"배송운영팀",
	"배송관리팀",
	"관제팀",
	"긴급배송팀",
	"냉장/냉동물류본부",
	"냉장물류팀",
	"냉동물류팀",
	"신선식품배송팀",
	"새벽배송팀",
	"차량관리본부",
	"차량정비팀",
	"차량관제팀",
	"유류관리팀",
	"기사관리팀",
	"창고운영본부",
	"입고팀",
	"출고팀",
	"재고관리팀",
	"냉장창고팀",
	"냉동창고팀",
	"영업본부",
	"물류영업팀",
	"거래처관리팀",
	"고객지원팀(CS)",
	"IT본부",
	"ERP개발팀",
	"인프라운영팀",
	"보안관리팀",
];
export default function CSelect({optionList = departmentList, value = "IT본부", onChange, width}) {
	
	const [selectedOption, setSelectedOption] = useState(value);
	
	return (
		<select
			className={s.cSelect}
			value={value}
			style={{
				width: width ? `${width}px` : 'auto',
			}}
			onChange={(e) => {
				setSelectedOption(e.target.value)
				onChange?.(e)
			}}
		>
			{optionList.map((item, idx) => (
				<option value={item} key={idx}>{item}</option>
			))}
		</select>
	)
}