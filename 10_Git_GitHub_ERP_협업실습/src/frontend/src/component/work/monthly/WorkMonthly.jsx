'use client';

import BreadCrumb from '@/component/common/BreadCrumb';
import MainTitleWrapper from '@/component/common/MainTitleWrapper';
import clsx from 'clsx';
import { CalendarDays, Grid3X3, ChevronLeft, ChevronRight, Search } from 'lucide-react';
import c from "./WorkMonthly.module.css"
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from '@/components/ui/select';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { useEffect, useState } from 'react';
import { parsingDate, parsingMonthKorean } from '@/common/utils/dateUtils';
import { Calendar } from '@/components/ui/calendar';
import CButton from '@/component/common/element/CButton';
import CSelect from '@/component/common/element/CSelect';
import baseApi from '@/common/api/baseApi';
const employees = [
	{
		name: '김철수',
		dept: '인사팀',
		days: {
			1: '출',
			2: '출',
			3: '지',
			4: '출',
			5: '휴',
			6: '휴',
			7: '출',
			8: '연',
			9: '출',
			10: '출',
			11: '장',
			12: '휴',
			13: '휴',
			14: '장',
			15: '출',
			16: '출',
			17: '출',
			18: '출',
			19: '휴',
			20: '휴',
			21: '출',
			22: '반',
			23: '출',
			24: '출',
			25: '출',
			26: '휴',
			27: '휴',
			28: '출',
			29: '출',
			30: '출',
			31: '출',
		},
		summary: {
			출근: 20,
			지각: 1,
			연차: 1,
			결근: 0,
		},
	},
	{
		name: '이영희',
		dept: '경영지원팀',
		days: {
			1: '출',
			2: '출',
			3: '출',
			4: '연',
			5: '휴',
			6: '휴',
			7: '연',
			8: '출',
			9: '출',
			10: '지',
			11: '출',
			12: '휴',
			13: '휴',
			14: '출',
			15: '출',
			16: '반',
			17: '출',
			18: '출',
			19: '휴',
			20: '휴',
			21: '출',
			22: '출',
			23: '장',
			24: '장',
			25: '출',
			26: '휴',
			27: '휴',
			28: '출',
			29: '출',
			30: '출',
			31: '출',
		},
		summary: {
			출근: 19,
			지각: 1,
			연차: 2,
			결근: 0,
		},
	},
];
const statusList = [
	['출근', '#CBD5E1'],
	['지각', '#FDBA74'],
	['연차', '#86EFAC'],
	['반차', '#7DD3FC'],
	['출장', '#C4B5FD'],
	['결근', '#FCA5A5'],
	['휴일', '#CBD5E1'],
];
const days = Array.from({ length: 31 }, (_, i) => i + 1);

export default function WorkMonthly() {

	const [openPopover, setOpenPopover] = useState(false);
	const [date, setDate] = useState(parsingDate(new Date()));

	const getMonthlyList = async () => {
		const token = localStorage.getItem("accessToken");
		const res = await baseApi.get("/api/v1/attendances/monthly", {
			headers: {
				Authorization: `Bearer ${token}`
			}
		});
	}

	useEffect(() => {
		getMonthlyList()
	}, [])

	return (
		<main className={clsx("w-[1190px] bg-[#F3F6FA] p-[10px] text-[#1F2937]", c.mainWrapper)}>
			<BreadCrumb
				crumList={[
					{ type: 'icon', path: '/breadcrumb/breadcrumb-home.png', title: '' },
					{ type: 'title', path: '/breadcrumb/breadcrumb-home.png', title: '근태관리' },
					{ type: 'title', path: '/breadcrumb/breadcrumb-home.png', title: '근태관리' },
					{ type: 'title', path: '/breadcrumb/breadcrumb-home.png', title: '월근태현황' },
				]}
			/>

			<MainTitleWrapper
				buttonRender={() => { }}
				mainTitleData={{
					title: "월근태현황",
					desc: "부서별·직원별 월간 근태 현황을 조회하고 관리합니다."
				}}
			/>

			<div className="w-[1167px] rounded-[12px] border border-[#E5E7EB] bg-white px-[32px] py-[22px] shadow-sm">
				<div className="flex items-center justify-between">
					{/* left area */}
					<div className="flex items-center gap-[28px]">
						{/* month picker */}
						<div className="flex h-[34px] overflow-hidden rounded-[10px] border border-[#D1D5DB] bg-white">
							<button className="flex w-[56px] items-center justify-center border-r border-[#D1D5DB] bg-[#F8FAFC]">
								<ChevronLeft
									size={22}
									className="text-[#334155] "
									onClick={() => {
										const originDate = new Date(date);
										originDate.setMonth(originDate.getMonth() - 1);
										setDate(parsingDate(originDate));
									}}
								/>
							</button>

							<div className="flex w-[180px] items-center justify-center gap-2 text-[14px] font-bold">
								{/* <CalendarDays size={15} className="text-[#183A6B]" /> */}
								<Popover open={openPopover} onOpenChange={setOpenPopover} className="flex">
									<PopoverTrigger>
										<div
											className={c.calendarWrapper}
											onClick={() => setOpenPopover(true)}

										>
											<span className={c.searchFromDate}>{parsingMonthKorean(date)}</span>
											<CalendarDays
												size={13}
												className={c.calendar}
												color="#9CA3AF"
											/>
										</div>
									</PopoverTrigger>

									<PopoverContent>
										<Calendar
											mode="single"
											selected={date}
											onSelect={(date) => {
												if (date) {
													setDate(parsingMonthKorean(date));
												}

												setOpenPopover(false);
											}}
										/>
									</PopoverContent>
								</Popover>
							</div>

							<button className="flex w-[56px] h-[34px] items-center justify-center border-l border-[#D1D5DB] bg-[#F8FAFC]">
								<ChevronRight
									size={22}
									className="text-[#334155]"
									onClick={() => {
										const originDate = new Date(date);
										originDate.setMonth(originDate.getMonth() + 1);
										setDate(parsingDate(originDate));
									}}
								/>
							</button>
						</div>

						{/* department */}
						<div className="flex items-center gap-[14px]">
							<span className="text-[13px] font-[700] text-[#111827]">부서</span>


							<CSelect
								optionList={[
									"전체 부서",
									"개발팀",
									"경영지원팀"
								]}
							/>
						</div>

						{/* search button */}
						<button className="flex">

							<CButton
								beforeIcon={<Search size={22} />}
								buttonName="조회"
								type='type2'
							/>
						</button>
					</div>

					{/* legend */}
					<div className="flex items-center gap-[14px]">
						{statusList.map(([label, color]) => (
							<div key={label} className="flex items-center gap-[7px]">
								<span
									className="h-[10px] w-[10px] rounded-[5px]"
									style={{ backgroundColor: color }}
								/>
								<span className="text-[11px] font-[500] text-[#64748B]">
									{label}
								</span>
							</div>
						))}
					</div>
				</div>
			</div>

			<section className="overflow-hidden rounded-[8px] border border-[#E5E7EB] bg-white">
				<div className="flex h-[42px] items-center justify-between px-4">
					<div className="flex items-center gap-2 text-[15px] font-bold text-[#183A6B]">
						<Grid3X3 size={15} />
						2025년 7월 근태현황
					</div>

					<div className="flex items-center gap-5 text-[12px] font-bold text-[#4B5563]">
						<span>
							<b className="mr-1 text-[#64748B]">●</b>총 근무일 23일
						</span>
						<span>
							<b className="mr-1 text-[#3B82F6]">●</b>대상 인원 5명
						</span>
					</div>
				</div>

				<div className="overflow-x-auto">
					<table className="w-full table-fixed border-collapse text-center text-[12px]">
						<thead>
							<tr className="h-[36px] bg-[#F1F5F9] text-[#64748B]">
								<th className="w-[70px] border border-[#E5E7EB] font-bold">
									성명
								</th>
								<th className="w-[92px] border border-[#E5E7EB] font-bold">
									부서
								</th>

								{days.map((day) => (
									<th
										key={day}
										className={`w-[25px] border border-[#E5E7EB] font-bold ${day === 5 ||
											day === 6 ||
											day === 12 ||
											day === 13 ||
											day === 19 ||
											day === 20 ||
											day === 26 ||
											day === 27
											? 'bg-[#EAF1F8] text-[#94A3B8]'
											: ''
											}`}
									>
										{day}
									</th>
								))}

								<th className="w-[42px] border border-[#DBEAFE] bg-[#EFF6FF] font-bold text-[#2563EB]">
									출근
								</th>
								<th className="w-[42px] border border-[#FED7AA] bg-[#FFF7ED] font-bold text-[#EA580C]">
									지각
								</th>
								<th className="w-[42px] border border-[#BBF7D0] bg-[#F0FDF4] font-bold text-[#16A34A]">
									연차
								</th>
								<th className="w-[42px] border border-[#FECACA] bg-[#FFF1F2] font-bold text-[#E11D48]">
									결근
								</th>
							</tr>
						</thead>

						<tbody>
							{employees.map((emp) => (
								<tr key={emp.name} className="h-[36px] bg-white">
									<td className="border border-[#E5E7EB] font-bold text-[#111827]">
										{emp.name}
									</td>
									<td className="border border-[#E5E7EB] font-bold text-[#64748B]">
										{emp.dept}
									</td>

									{days.map((day) => (
										<td
											key={day}
											className={`border border-[#E5E7EB] ${getDayBg(
												emp.days[day],
												day
											)}`}
										>
											<StatusText value={emp.days[day]} />
										</td>
									))}

									<td className="border border-[#DBEAFE] bg-[#EFF6FF] font-bold text-[#2563EB]">
										{emp.summary.출근}
									</td>
									<td className="border border-[#FED7AA] bg-[#FFF7ED] font-bold text-[#EA580C]">
										{emp.summary.지각}
									</td>
									<td className="border border-[#BBF7D0] bg-[#F0FDF4] font-bold text-[#16A34A]">
										{emp.summary.연차}
									</td>
									<td className="border border-[#FECACA] bg-[#FFF1F2] font-bold text-[#CBD5E1]">
										{emp.summary.결근}
									</td>
								</tr>
							))}
						</tbody>
					</table>
				</div>
			</section>
		</main>
	);
}

function StatusText({ value }) {
	const map = {
		출: 'text-[#94A3B8]',
		지: 'text-[#EA580C] font-bold',
		연: 'text-[#16A34A] font-bold',
		장: 'text-[#8B5CF6] font-bold',
		반: 'text-[#0284C7] font-bold',
		휴: 'text-[#CBD5E1]',
	};

	return <span className={map[value] || 'text-[#94A3B8]'}>{value}</span>;
}

function getDayBg(value, day) {
	const weekend = [5, 6, 12, 13, 19, 20, 26, 27].includes(day);

	if (value === '지') return 'bg-[#FFF7ED]';
	if (value === '연') return 'bg-[#F0FDF4]';
	if (value === '장') return 'bg-[#F5F3FF]';
	if (value === '반') return 'bg-[#E0F2FE]';
	if (weekend) return 'bg-[#EAF1F8]';
	return 'bg-white';
}
