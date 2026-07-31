'use client'

import c from './AppointmentForm.module.css';
import {ArrowRight, CalendarDays, FilePen, Lock, Save, User, X,} from "lucide-react";
import {Popover, PopoverContent, PopoverTrigger} from "@/components/ui/popover";
import {useEffect, useState} from "react";
import {Calendar} from "@/components/ui/calendar";
import CInput from "@/component/common/element/CInput";
import CButton from "@/component/common/element/CButton";
import {clsx} from "clsx";

const parsingDate = (targetDate) => {
	const newDate = new Date(targetDate);
	
	const year = newDate.getFullYear();
	const month = newDate.getMonth() + 1 < 10 ? `0${newDate.getMonth() + 1}` : newDate.getMonth() + 1;
	const date = newDate.getDate() < 10 ? `0${newDate.getDate()}` : newDate.getDate();
	
	
	const parsedDate = `${year}-${month}-${date}`;
	return parsedDate
}


const appointTypeList = [
	"승진",
	"전보",
	"겸직",
	"기타"
]

export default function AppointmentForm({setIsShowForm}) {
	
	const [date, setDate] = useState(parsingDate(new Date()));
	const [openFormPopover, setOpenFormPopover] = useState(false);
	const [activeAppointmentType, setActiveAppointmentType] = useState(appointTypeList[0]);
	const [userInfo, setUserInfo] = useState({});
	
	useEffect(() => {
		const jsonUser = localStorage.getItem("user")
		const userInfo = JSON.parse(jsonUser);
		setUserInfo(userInfo);
	}, []);
	
	
	return (
		<div className={c.container}>
			<section className={c.titleSection}>
				<div className={c.titleWrapper}>
					<FilePen color="#1B3A6B" className='w-[15px]'/>
					<span>발령 입력 폼</span>
				</div>
				
				{userInfo && (
					<div className={c.userStatusWrapper}>
						<User color="#2563EB" size={13}/>
						<ul className={c.userStatusList}>
							<li>{userInfo?.employeeNo}</li>
							<li>{userInfo?.name}</li>
							<li>{userInfo?.departmentName}</li>
							<li>{userInfo?.positionName}</li>
						</ul>
					</div>
				)}
			
			</section>
			
			<section className={c.formSection}>
				
				{/* 1.발령입력폼 발령유형, 발령일...*/}
				<div className={c.appointmentDataWrapper}>
					
					<div className={c.appointmentDataItem}>
						<label>발령유형 <span className='text-[#EF4444]'>*</span></label>
						<div className={c.tabWrapper}>
							<ul className={c.tabs}>
								{appointTypeList.map((item, index) => (
									<li
										key={index}
										className={clsx(item === activeAppointmentType ? c.active : "")}
										onClick={() => setActiveAppointmentType(item)}
									>
										{item}
									</li>
								))}
							
							</ul>
						</div>
					</div>
					
					<div className={c.appointmentDataItem}>
						<label>발령일 <span className='text-[#EF4444]'>*</span></label>
						
						<div className={c.tabWrapper}>
							<Popover open={openFormPopover} onOpenChange={setOpenFormPopover}>
								<PopoverTrigger>
									<div className={c.triggerDateWrapper}>
										<span className={c.triggerDate}>{date}</span>
										<CalendarDays size={13} className={c.calendar} color='#9CA3AF'/>
									</div>
								</PopoverTrigger>
								
								<PopoverContent>
									<Calendar
										mode="single"
										selected={date}
										onSelect={(date) => {
											setDate(parsingDate(date));
											setOpenFormPopover(false)
										}}
									/>
								</PopoverContent>
							</Popover>
						</div>
					</div>
					
					<div className={c.appointmentDataItem}>
						<label>발령번호</label>
						
						<div>
              <span className={c.appointmentNumber}>
                자동생성
              </span>
						</div>
					</div>
					
					<div className={c.appointmentDataItem}>
						<label>발령사유</label>
						
						<div>
							<CInput
								placeholder='발령 사유를 입력하세요'
								width={260}
							/>
						</div>
					</div>
				</div>
				
				{/* 2.발령입력폼 -> 발령전, 발령후*/}
				<div className={c.appointmentPositionStatusWrapper}>
					<div className={c.appointmentBefore}>
						<div className={c.beforeTop}>
							<span>발령 전</span>
						</div>
						
						<div className={c.beforeContent}>
							<div className={c.beforeItem}>
								<label htmlFor="부서">부서</label>
								<div>
									<input type="text" id='부서' placeholder='경영지원팀'/>
									<Lock color='#9CA3AF' className={c.inputIcon} size={12}/>
								</div>
							</div>
							
							<div className={c.beforeItem}>
								<label htmlFor="직급">직급</label>
								<div>
									<input type="text" id='직급' placeholder='과장'/>
									<Lock color='#9CA3AF' className={c.inputIcon} size={12}/>
								</div>
							</div>
							
							<div className={c.beforeItem}>
								<label htmlFor="직책">직책</label>
								<div>
									<input type="text" id='직책' placeholder='팀원'/>
									<Lock color='#9CA3AF' className={c.inputIcon} size={12}/>
								</div>
							</div>
						</div>
					</div>
					
					<div className={c.arrowWrapper}>
						<ArrowRight color="black" size={22}/>
					</div>
					
					{/*발령후*/}
					<div className={c.appointmentAfter}>
						<div className={c.afterTop}>
							<span>발령 후</span>
						</div>
						
						<div className={c.afterContent}>
							<div className={c.afterItem}>
								<label htmlFor="부서">부서</label>
								<div>
									<select>
										<option value="인사팀">인사팀</option>
										<option value="인사팀">인사팀</option>
										<option value="인사팀">인사팀</option>
										<option value="인사팀">인사팀</option>
									</select>
								</div>
							</div>
							
							<div className={c.afterItem}>
								<label htmlFor="직급">직급</label>
								<div>
									<select>
										<option value="차장">차장</option>
										<option value="차장">차장</option>
										<option value="차장">차장</option>
										<option value="차장">차장</option>
									</select>
								</div>
							</div>
							
							<div className={c.afterItem}>
								<label htmlFor="직책">직책</label>
								<div>
									<select>
										<option value="팀원">팀원</option>
										<option value="팀원">팀원</option>
										<option value="팀원">팀원</option>
										<option value="팀원">팀원</option>
									</select>
								</div>
							</div>
						</div>
					</div>
				</div>
				
				
				{/*3. 비고, 취소,저장*/}
				<div className={c.etcWrapper}>
					<div className={c.etcTextArea}>
						<p>비고</p>
						<textarea name="" id="" cols="30" rows="10" placeholder='발령 관련 추가 사항을 입력하세요.'/>
					</div>
					<div className={c.etcButtonWrapper}>
						<CButton
							type='type1'
							buttonName='취소'
							beforeIcon={<X color="#6B7280" size={13}/>}
							onClick={() => {
								setIsShowForm?.(false)
							}}
						/>
						<CButton
							type='type2'
							buttonName='저장'
							beforeIcon={<Save color="#fff" size={13}/>}
						/>
					</div>
				</div>
			</section>
			
			<section>
			
			</section>
		</div>
	)
}