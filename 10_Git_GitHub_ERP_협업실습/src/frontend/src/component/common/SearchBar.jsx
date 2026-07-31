'use client';

import CButton from './element/CButton';
import CInput from './element/CInput';
import CLabel from './element/CLabel';
import CSelect from './element/CSelect';
import s from './SearchBar.module.css';
import {CalendarDays, Search} from 'lucide-react';
import {useState} from "react";
import {usePathname} from "next/navigation";
import c from "@/component/appointment/AppointmentForm.module.css";
import {Popover, PopoverContent, PopoverTrigger} from "@/components/ui/popover";
import {Calendar} from "@/components/ui/calendar";

const initialSearchInfo = {
	keyword: "",
	departmentName: "전체",
	positionName: "전체",
	employeeStatusCode: "전체"
}


const appointTypeList = [
	"전체",
	"승진",
	"전보",
	"겸직",
	"기타"
]


const parsingDate = (targetDate) => {
	const newDate = new Date(targetDate);
	
	const year = newDate.getFullYear();
	const month = newDate.getMonth() + 1 < 10 ? `0${newDate.getMonth() + 1}` : newDate.getMonth() + 1;
	const date = newDate.getDate() < 10 ? `0${newDate.getDate()}` : newDate.getDate();
	
	
	const parsedDate = `${year}-${month}-${date}`;
	return parsedDate
}

export default function SearchBar({useKeyword, useDpt, usePeriod, useExactDate, useCustomRender, goSearch, type = ""}) {
	
	const [searchInfo, setSearchInfo] = useState({})
	const [searchFromDate, setSearchFromDate] = useState(parsingDate(new Date()));
	const [searchToDate, setSearchToDate] = useState(parsingDate(new Date()));
	const [openPopover, setOpenPopover] = useState(false);
	const [openToPopover, setOpenToPopover] = useState(false);
	
	const renderBasic = () => {
		return (
			<>
				<div className={s.conditionItem}>
					<CLabel
						labelName='사원번호'
					/>
					<CInput
						value={searchInfo?.keyword || ''}
						onChange={e => setSearchInfo({...searchInfo, keyword: e.target.value})}
						onKeyDown={e => {
							if (e.key === 'Enter') {
								goSearch?.(searchInfo)
							}
						}}
					/>
				</div>
				
				<div className={s.conditionItem}>
					<CLabel
						labelName='부서'
					/>
					<CSelect
						value={searchInfo?.departmentName || ''}
						onChange={e => setSearchInfo({...searchInfo, departmentName: e.target.value})}
					/>
				</div>
				
				<div className={s.conditionItem}>
					<CLabel
						labelName='직급'
					/>
					<CSelect
						optionList={[
							"전체",
							"사원",
						]}
						value={searchInfo?.positionName || ''}
						onChange={e => setSearchInfo({...searchInfo, positionName: e.target.value})}
					/>
				</div>
				
				<div className={s.conditionItem}>
					<CLabel
						labelName='재직상태'
					/>
					<CSelect
						optionList={[
							"전체",
							"재직",
							"휴직중",
							"퇴사"
						]}
						value={searchInfo?.employeeStatusCode || ''}
						onChange={e => setSearchInfo({...searchInfo, employeeStatusCode: e.target.value})}
					/>
				</div>
				
				<div className={s.conditionItem}>
					<CButton
						path='/search-w.png'
						type='type2'
						buttonName='조회'
						onClick={() => goSearch?.(searchInfo)}
					/>
					
					<CButton
						path='/rotate.png'
						type='type1'
						buttonName='초기화'
						onClick={() => {
							console.log("초기화 클릭")
							setSearchInfo({...initialSearchInfo})
						}}
					/>
				</div>
			</>
		)
	}
	const renderAppointment = () => {
		return (
			<>
				<div className={s.conditionItem}>
					<label
						htmlFor=""
						className={s.appointmentSearchLabel}
					>
						사원검색
					</label>
					<input
						type="text"
						className={s.appointmentSearchInput}
						placeholder="사원번호 또는 성명"
					/>
					<div className={s.searchMagnifyIcon}>
						<Search size={14} color="#fff"/>
					</div>
				</div>
				
				<div className={s.conditionItem}>
					<label
						htmlFor=""
						className={s.appointmentSearchLabel}
					>
						발령유형
					</label>
					
					<select
						className={s.appointmentSearchSelect}
					>
						{appointTypeList.map((item, idx) => (
							<option key={idx} value={item}>{item}</option>
						))}
					
					
					</select>
				
				</div>
				
				<div className={s.conditionItem}>
					<label
						htmlFor=""
						className={s.appointmentSearchLabel}
					>
						발령일
					</label>
					
					<div>
						<Popover open={openPopover} onOpenChange={setOpenPopover}>
							<PopoverTrigger>
								<div className="relative" onClick={() => setOpenPopover(true)}>
									<span className={s.searchFromDate}>{searchFromDate}</span>
									<CalendarDays size={13} className={c.calendar} color='#9CA3AF'/>
								</div>
							</PopoverTrigger>
							
							<PopoverContent>
								<Calendar
									mode="single"
									selected={searchFromDate}
									onSelect={date => {
										if (date) {
											setSearchFromDate(parsingDate(date));
										}
										
										setOpenPopover(false);
									}}
								/>
							</PopoverContent>
						</Popover>
					</div>
					
					<div className={s.searchWaveIcon}>
						~
					</div>
					
					<div>
						<Popover open={openToPopover} onOpenChange={setOpenToPopover}>
							<PopoverTrigger>
								<div className="relative" onClick={() => setOpenToPopover(true)}>
									<span className={s.searchFromDate}>{searchToDate}</span>
									<CalendarDays size={13} className={c.calendar} color='#9CA3AF'/>
								</div>
							</PopoverTrigger>
							
							<PopoverContent>
								<Calendar
									mode="single"
									selected={searchToDate}
									onSelect={date => {
										if (date) {
											setSearchToDate(parsingDate(date));
										}
										
										setOpenToPopover(false);
									}}
								/>
							</PopoverContent>
						</Popover>
					</div>
				
				
				</div>
				
				<div className={s.conditionItem}>
					<CButton
						path='/search-w.png'
						type='type2'
						buttonName='조회'
						onClick={() => goSearch?.(searchInfo)}
					/>
					
					<CButton
						path='/rotate.png'
						type='type1'
						buttonName='초기화'
						onClick={() => {
							console.log("초기화 클릭")
							setSearchInfo({...initialSearchInfo})
						}}
					/>
				</div>
			</>
		)
	}
	
	const pathname = usePathname();
	
	return (
		<div className={s.container}>
			<div className={s.searchBarTitle}>
				<Search size={15}/>
				<span>검색조건</span>
			</div>
			
			<div className={s.searchConditionWrapper}>
				{
					pathname.includes("/appointment")
						? renderAppointment()
						: renderBasic()
				}
			</div>
		</div>
	)
}