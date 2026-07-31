'use client';

import {
	CalendarDays,
	ChevronLeft,
	ChevronRight,
	Search,
	UserRound,
	Check,
	AlarmClock,
	LogOut,
	X,
	CalendarCheck,
	Briefcase,
	BookOpen,
	ShieldCheck,
	Clock,
	RotateCcw,
	Save,
	ListChecks,
	Plus,
	Edit,
	Trash2,
	Users,
} from 'lucide-react';
import BreadCrumb from '@/component/common/BreadCrumb';
import CButton from '@/component/common/element/CButton';
import { clsx } from 'clsx';

import MainTitleWrapper from '@/component/common/MainTitleWrapper';
import c from './WorkAttendance.module.css';
import { useEffect, useState } from 'react';
import {
	Popover,
	PopoverContent,
	PopoverTrigger,
} from '@/components/ui/popover';
import { Calendar } from '@/components/ui/calendar';
import { getAttnedTime, getNowTime, parsingDate, parsingIsoTime } from '@/common/utils/dateUtils';
import CSelect from '@/component/common/element/CSelect';
import baseApi from '@/common/api/baseApi';
import { toast } from 'sonner';
import LoadingSpinner from '@/common/LoadingSpinner';
const rows = [
	{
		no: 'EMP-001',
		name: '김철수',
		dept: '인사팀',
		rank: '팀장',
		type: '출근',
		in: '09:02',
		out: '18:05',
		ot: '-',
		memo: '-',
	},
	{
		no: 'EMP-002',
		name: '이영희',
		dept: '경영지원팀',
		rank: '과장',
		type: '지각',
		in: '09:27',
		out: '18:10',
		ot: '-',
		memo: '27분 지각',
	},
	{
		no: 'EMP-003',
		name: '박민준',
		dept: '개발팀',
		rank: '대리',
		type: '연차',
		in: '-',
		out: '-',
		ot: '-',
		memo: '연차 1일 사용',
	},
	{
		no: 'EMP-004',
		name: '최지영',
		dept: '영업팀',
		rank: '사원',
		type: '출장',
		in: '08:50',
		out: '19:30',
		ot: '1.5h',
		memo: '부산 출장',
	},
	{
		no: 'EMP-005',
		name: '정수빈',
		dept: '개발팀',
		rank: '사원',
		type: '반차',
		in: '09:05',
		out: '14:00',
		ot: '-',
		memo: '오후 반차',
	},
	{
		no: 'EMP-006',
		name: '한지민',
		dept: '영업팀',
		rank: '대리',
		type: '미등록',
		in: '-',
		out: '-',
		ot: '-',
		memo: '-',
	},
];

const types = [
	{ label: '출근', icon: Check, color: 'blue' },
	{ label: '지각', icon: AlarmClock, color: 'orange' },
	{ label: '조퇴', icon: LogOut, color: 'gray' },
	{ label: '결근', icon: X, color: 'red' },
	{ label: '연차', icon: CalendarCheck, color: 'green' },
	{ label: '반차', icon: CalendarDays, color: 'sky' },
	{ label: '퇴근', icon: Briefcase, color: 'purple' },
	{ label: '교육', icon: BookOpen, color: 'gray' },
	{ label: '공가', icon: ShieldCheck, color: 'gray' },
];

export default function WorkAttendance() {
	const [isOverTime, setIsOverTime] = useState(false);
	const [startTime, setStartTime] = useState(getNowTime());
	const [endTime, setEndTime] = useState(getNowTime());
	const [startOverTime, setStartOverTime] = useState('18:00');
	const [endOverTime, setEndOverTime] = useState('23:00');

	const [openPopover, setOpenPopover] = useState(false);
	const [date, setDate] = useState(parsingDate(new Date()));

	const [userInfo, setUserInfo] = useState({});

	const [attendanceList, setAttendanceList] = useState([]);
	const [selectedTab, setSelectedTab] = useState();
	const [memo, setMemo] = useState();
	const [statusMap, setStatusMap] = useState({})

	const [isLoading, setIsLoading] = useState(false);

	const goAttend = async () => {
		const token = localStorage.getItem("accessToken");
		try {
			setIsLoading(true)
			let path = "/api/v1/attendances/checkin"
			if (selectedTab === '퇴근') {
				path = "/api/v1/attendances/checkout"
			}

			const is출퇴근 = ["출근", "퇴근"].includes(selectedTab);
			if (!is출퇴근) {
				toast("개발 전 입니다.", { position: 'top-center' })
				return;
			}

			if (selectedTab === '퇴근') {

				const start = Number((startTime || '').replaceAll(":", ""));
				const end = Number((endTime || '').replaceAll(":", ""));
				if (start > end) {
					toast("퇴근시간이 잘못 입력되었습니다.", { position: "top-center" })
					return;
				}

			}

			const res = await baseApi.post(path, {
				workDate: selectedTab === '출근' ? parsingDate(new Date()) : parsingIsoTime(endTime),
				memo
			}, {
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			toast(`${selectedTab} 정상처리 되었습니다.`, { position: 'top-center' })
			getAttendanceDaily();

			setIsLoading(true)
		} catch (e) {
			toast(e?.response?.data?.message || "네트워크 에러", { position: 'top-center' });
		} finally {
			setIsLoading(false)
		}


	}

	useEffect(() => {
		const jsonUser = localStorage.getItem('user');
		const user = JSON.parse(jsonUser);

		setUserInfo({ ...user });
	}, []);

	const getAttendanceDaily = async (findDate) => {
		try {

			setIsLoading(true)
			const token = localStorage.getItem('accessToken');
			const res = await baseApi.get('/api/v1/attendances/daily', {
				params: {
					...(findDate && { findDate })
				},
				headers: {
					Authorization: `Bearer ${token}`,
				},
			});

			const statusMap = {
				전체: res?.data?.data?.length,
				출근: 0,
				퇴근: 0,
				지각: 0,
				결근: 0,
				연차: 0,
			}

			for (const a of res?.data?.data) {
				if (a?.checkInTime) statusMap.출근++;
			}
			setStatusMap({ ...statusMap })

			setAttendanceList(res?.data?.data);
		} catch (e) {

		} finally {
			setIsLoading(false)
		}
	};

	useEffect(() => {
		getAttendanceDaily();
	}, []);

	const buttonRender = () => {
		// return (
		// 	<>
		// 		<CButton
		// 			path="/download.png"
		// 			type="type1"
		// 			buttonName="PDF 다운로드"
		// 			onClick={() => {
		// 				setIsOpenAlert(true);
		// 			}}
		// 		/>
		// 		<CButton
		// 			path="/plus.png"
		// 			type="type2"
		// 			buttonName="신규등록"
		// 			onClick={() => {
		// 				setSelectedInfo({});
		// 				setIsEdit(false);
		// 				setOpen(true);
		// 			}}
		// 		/>
		// 	</>
		// );
	};

	return (
		<main className="w-[1190px] bg-[#F3F6FA] !p-[10px] text-[#1F2937]">
			<BreadCrumb
				crumList={[
					{ type: 'icon', path: '/breadcrumb/breadcrumb-home.png', title: '' },
					{ type: 'title', path: '/breadcrumb/breadcrumb-home.png', title: '근태관리' },
					{ type: 'title', path: '/breadcrumb/breadcrumb-home.png', title: '근태관리' },
					{ type: 'title', path: '/breadcrumb/breadcrumb-home.png', title: '일일근태등록' },
				]}
			/>
			<MainTitleWrapper
				buttonRender={buttonRender}
				mainTitleData={{
					title: "일일근태등록",
					desc: "날짜별 직원 근태 현황을 등록하고 수정합니다."
				}}

			/>
			<div className={c.mainContentWrapper}>
				<TopBar
					openPopover={openPopover}
					setOpenPopover={setOpenPopover}
					date={date}
					setDate={setDate}
					statusMap={statusMap}
					getAttendanceDaily={getAttendanceDaily}
				/>

				<div className="mt-14 grid grid-cols-[330px_1fr] gap-3">
					<RegisterCard
						memo={memo}
						setMemo={setMemo}
						selectedTab={selectedTab}
						setSelectedTab={setSelectedTab}
						goAttend={goAttend}
						userInfo={userInfo}
						isOverTime={isOverTime}
						setIsOverTime={setIsOverTime}
						startTime={startTime}
						endTime={endTime}
						setStartTime={setStartTime}
						setEndTime={setEndTime}
						startOverTime={startOverTime}
						endOverTime={endOverTime}
						setStartOverTime={setStartOverTime}
						setEndOverTime={setEndOverTime}
					/>
					<TableCard date={date} attendanceList={attendanceList} />
				</div>
			</div>

			<LoadingSpinner isLoading={isLoading} />
		</main>
	);
}

function TopBar({ openPopover, setOpenPopover, date, setDate, statusMap, getAttendanceDaily }) {
	return (
		<div className="flex h-[60px] items-center justify-between rounded-[6px] border border-[#E5E7EB] bg-white !px-5 mt-">
			<div className="flex items-center gap-4">
				<div className="flex h-[34px] overflow-hidden rounded-[5px] border border-[#D1D5DB]">
					<button className="w-[34px] border-r bg-[#F8FAFC]">
						<ChevronLeft
							size={16}
							className="mx-auto"
							onClick={() => {
								const originDate = new Date(date);
								originDate.setDate(originDate.getDate() - 1);
								setDate(parsingDate(originDate));
								getAttendanceDaily(originDate)
							}}
						/>
					</button>
					<div className="flex w-[180px] items-center justify-center gap-2 text-[14px] font-bold">
						{/* <CalendarDays size={15} className="text-[#183A6B]" /> */}
						<Popover open={openPopover} onOpenChange={setOpenPopover}>
							<PopoverTrigger>
								<div
									className={c.calendarWrapper}
									onClick={() => setOpenPopover(true)}
								>
									<span className={c.searchFromDate}>{date}</span>
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
											setDate(parsingDate(date));
										}

										setOpenPopover(false);
									}}
								/>
							</PopoverContent>
						</Popover>
					</div>
					<button className="w-[34px] border-l bg-[#F8FAFC]">
						<ChevronRight
							size={16}
							className="mx-auto"
							onClick={() => {
								const originDate = new Date(date);
								originDate.setDate(originDate.getDate() + 1);
								setDate(parsingDate(originDate));
								getAttendanceDaily(originDate)
							}}
						/>
					</button>
				</div>

				<button className="flex h-[34px] items-center gap-1 rounded-[5px] border border-[#BFDBFE] bg-[#EFF6FF] !px-4 text-[13px] font-bold text-[#2563EB]">
					<CalendarDays size={14} />
					오늘
				</button>

				<div className="flex items-center gap-2">
					<span className="text-[14px] font-bold">부서</span>
					<CSelect />
				</div>

				<div className="relative">
					<Search
						size={15}
						className="absolute left-3 top-1/2 -translate-y-1/2 text-[#CBD5E1]"
					/>
					<input
						placeholder="사원명 검색"
						className="h-[34px] w-[130px] rounded-[5px] border border-[#D1D5DB] pl-9 text-[13px] outline-none"
					/>
				</div>
			</div>

			<div className="flex items-center gap-2">
				<Chip text={`전체${statusMap.전체}명`} color="gray" />
				<Chip text={`출근${statusMap.출근}`} color="blue" />
				<Chip text={`지각${statusMap.지각}`} color="orange" />
				<Chip text={`결근${statusMap.결근}`} color="red" />
				<Chip text={`연차${statusMap.연차}`} color="green" />
			</div>
		</div>
	);
}

function RegisterCard({
	isOverTime,
	setIsOverTime,
	startTime,
	endTime,
	setStartTime,
	setEndTime,
	startOverTime,
	endOverTime,
	setStartOverTime,
	setEndOverTime,
	userInfo = {},
	goAttend,
	selectedTab,
	setSelectedTab,
	memo,
	setMemo
}) {
	const todayMonth = new Date().getMonth() + 1 + '월';
	const todayDate = new Date().getDate() + '일';

	return (
		<section className="rounded-[6px] border border-[#E5E7EB] bg-white">
			<div className="flex h-[44px] items-center justify-between border-b !px-4">
				<div className="flex items-center gap-2 text-[15px] font-bold text-[#183A6B]">
					<ListChecks size={16} />
					근태 등록
				</div>
				<span className="rounded-full bg-[#DBEAFE] !px-3 !py-1 text-[12px] font-bold text-[#2563EB]">
					{`${todayMonth} ${todayDate}`}
				</span>
			</div>

			<div className={clsx('!p-4', c.formWrapper)}>
				<Label required>사원 선택</Label>
				<div className="mb-4 flex h-[36px] items-center justify-between rounded-[5px] border border-[#2563EB] !px-3">
					<div className="flex items-center gap-2">
						<span className="flex h-6 w-6 items-center justify-center rounded-full bg-[#DBEAFE] text-[11px] font-bold text-[#2563EB]">
							{(userInfo?.name || '').slice(0, 1)}
						</span>
						<b className="text-[13px]">
							{userInfo?.name} · {userInfo?.departmentName}
						</b>
					</div>
					<X size={14} className="text-[#9CA3AF]" />
				</div>

				<Label required>근태 유형</Label>
				<div className="grid grid-cols-3 gap-2">
					{types.map((item, idx) => (
						<TypeButton onClick={() => setSelectedTab(item.label)} key={item.label} {...item} selected={item.label === selectedTab} />
					))}
				</div>

				<div className="mt-4 grid grid-cols-2 gap-2">
					<TimeInput
						label="출근 시간"
						value={startTime}
						setTime={setStartTime}
						readOnly
					/>
					<TimeInput label="퇴근 시간" value={endTime} setTime={setEndTime} />
				</div>

				<div className="mt-4 flex items-center justify-between">
					<Label>초과근무(OT)</Label>
					<div className="flex items-center gap-2">
						<span
							className={clsx(
								'h-5 w-9 rounded-full  p-[2px] ',
								isOverTime ? 'bg-[#183A6B]' : 'bg-[#aaa1a1]'
							)}
							onClick={() => setIsOverTime(!isOverTime)}
						>
							<span
								className={clsx(
									'block h-4 w-4 rounded-full transition-transform duration-300',
									isOverTime ? 'bg-white translate-x-4' : 'bg-[#183A6B]'
								)}
							/>
						</span>
						<span className="text-[12px]">적용</span>
					</div>
				</div>

				{isOverTime && (
					<div className="grid grid-cols-[1fr_20px_1fr_50px] items-center gap-2">
						<SmallTime value={startOverTime} setTime={setStartOverTime} />
						<span className="text-center text-[#9CA3AF]">~</span>
						<SmallTime value={endOverTime} setTime={setEndOverTime} />
						{/* <div className="flex h-[36px] items-center justify-center rounded-[5px] border border-[#BBF7D0] bg-[#DCFCE7] text-[13px] font-bold text-[#22C55E]">
							2.5h
						</div> */}
					</div>
				)}

				<div className="mt-4">
					<Label>비고</Label>
					<textarea
						placeholder="특이사항을 입력하세요"
						className="h-[58px] w-full resize-none rounded-[5px] border border-[#D1D5DB] p-3 text-[13px] outline-none"
						value={memo}
						onChange={(e) => setMemo(e.target.value)}
					/>
				</div>

				<div className="mt-4 flex justify-end gap-2">
					<button className="flex h-[36px] w-[82px] items-center justify-center gap-1 rounded-[5px] border bg-white text-[13px] font-bold text-[#4B5563]">
						<RotateCcw size={14} />
						초기화
					</button>
					<button className="flex h-[36px] w-[82px] items-center justify-center gap-1 rounded-[5px] bg-[#183A6B] text-[13px] font-bold text-white" onClick={() => goAttend()}>
						<Save size={14} />
						저장
					</button>
				</div>
			</div>
		</section>
	);
}

function TableCard({ date, attendanceList }) {
	return (
		<section className="overflow-hidden rounded-[6px] border border-[#E5E7EB] bg-white">
			<div className="flex h-[44px] items-center justify-between border-b bg-[#F8FAFC] !px-4">
				<div className="flex items-center gap-2 text-[15px] font-bold text-[#183A6B]">
					<ListChecks size={16} />
					{date} 근태 목록
				</div>

				<div className="flex items-center gap-2">
					<span className="rounded-full bg-[#DBEAFE] !px-3 !py-1 text-[12px] font-bold text-[#2563EB]">
						총 {attendanceList.length}명
					</span>
					<button className="flex h-[32px] items-center gap-1 rounded-[5px] border border-[#BBF7D0] bg-[#F0FDF4] !px-3 text-[13px] font-bold text-[#16A34A]">
						<Users size={14} />
						일괄등록
					</button>
				</div>
			</div>

			<table className="w-full table-fixed border-collapse text-[13px]">
				<thead>
					<tr className="h-[42px] bg-[#F8FAFC] text-[#6B7280]">
						<th className="w-[40px]">
							<input type="checkbox" defaultChecked />
						</th>
						<Th>사원번호</Th>
						<Th>성명</Th>
						<Th>부서</Th>
						<Th>직급</Th>
						<Th>근태유형</Th>
						<Th>출근시간</Th>
						<Th>퇴근시간</Th>
						<Th>OT</Th>
						<Th>비고</Th>
						<Th>관리</Th>
					</tr>
				</thead>

				<tbody>
					{attendanceList.map((row, idx) => (
						<tr
							key={row.no}
							className={`h-[40px] border-t text-center ${row.type === '미등록' ? 'bg-[#FFFBEB]' : 'bg-white'
								}`}
						>
							<td>
								<input type="checkbox" />
							</td>
							<Td>{row.employeeNo}</Td>
							<Td bold>{row.name}</Td>
							<Td>{row.departmentName}</Td>
							<Td>{row.positionName}</Td>
							<Td>
								<StatusBadge type={row.checkInTime ? '출근' : '미등록'} />
							</Td>
							<Td
								color={
									Number((row?.checkInTime || '').replaceAll(':', '')) > 905
										? 'orange'
										: ''
								}
							>
								{getAttnedTime(row.checkInTime) || '-'}
							</Td>
							<Td>{getAttnedTime(row?.checkOutTime) || '-'}</Td>
							<Td color={row.ot !== '-' ? 'purple' : ''}>
								{getAttnedTime(row?.overtime) || '-'}
							</Td>
							<Td
								color={
									row.type === '지각'
										? 'orange'
										: row.type === '연차'
											? 'green'
											: row.type === '반차'
												? 'sky'
												: ''
								}
							>
								{row.comment || '-'}
							</Td>
							<td>
								{row.type === '미등록' ? (
									<button className="rounded-[4px] bg-[#FEF3C7] px-2 !py-1 text-[12px] font-bold text-[#D97706]">
										+ 등록
									</button>
								) : (
									<div className="flex justify-center gap-1">
										<button className="rounded-[4px] bg-[#EFF6FF] px-2 !py-1 text-[12px] font-bold text-[#2563EB]">
											수정
										</button>
										<button className="rounded-[4px] bg-[#FEF2F2] px-2 !py-1 text-[12px] font-bold text-[#EF4444]">
											삭제
										</button>
									</div>
								)}
							</td>
						</tr>
					))}
				</tbody>

				<tfoot>
					<tr className="h-[42px] border-t border-[#BFDBFE] bg-[#EFF6FF] text-center font-bold text-[#183A6B]">
						<td colSpan={5}></td>
						<td>합계</td>
						<td>{attendanceList.length}명 조회</td>
						<td>
							{/* 							평균
							<br />
							09:05 */}
						</td>
						<td>
							{/* 							평균
							<br />
							18:09 */}
						</td>
						<td className="text-[#7C3AED]">
							{/* 3.0h */}
						</td>
						<td></td>
					</tr>
				</tfoot>
			</table>

			<div className="flex h-[44px] items-center justify-between border-t px-4">
				<p className="text-[13px] text-[#6B7280]">
					{/* 전체 {attendanceList.length}명 중 6명 표시 · 미등록 1명 */}
					전체 {attendanceList.length}명
				</p>

				<div className="flex gap-1">
					<PageBtn>
						<ChevronLeft size={14} />
					</PageBtn>
					<PageBtn active>1</PageBtn>
					{/* <PageBtn>2</PageBtn> */}
					{/* <PageBtn>3</PageBtn> */}
					{/* <PageBtn>4</PageBtn> */}
					<PageBtn>
						<ChevronRight size={14} />
					</PageBtn>
				</div>
			</div>
		</section>
	);
}

function Chip({ text, color }) {
	const map = {
		gray: 'bg-[#F1F5F9] text-[#334155]',
		blue: 'bg-[#EFF6FF] text-[#2563EB]',
		orange: 'bg-[#FFF7ED] text-[#EA580C]',
		red: 'bg-[#FFF1F2] text-[#E11D48]',
		green: 'bg-[#F0FDF4] text-[#16A34A]',
	};

	return (
		<span
			className={`rounded-full px-3 !py-1 text-[12px] font-bold ${map[color]}`}
		>
			● {text}
		</span>
	);
}

function Label({ children, required }) {
	return (
		<label className="mb-2 block text-[13px] font-bold">
			{children} {required && <span className="text-red-500">*</span>}
		</label>
	);
}

function TypeButton({ label, icon: Icon, selected, color, onClick }) {
	const selectedClass = selected
		? 'border-[#183A6B] bg-[#183A6B] text-white'
		: 'border-[#D1D5DB] bg-white text-[#6B7280]';

	const colorClass = {
		orange: 'text-[#EA580C] border-[#FDBA74]',
		red: 'text-[#EF4444] border-[#FECACA]',
		green: 'text-[#16A34A] border-[#BBF7D0]',
		sky: 'text-[#0284C7] border-[#BAE6FD]',
		purple: 'text-[#8B5CF6] border-[#DDD6FE]',
		gray: 'text-[#6B7280]',
	};

	return (
		<button
			className={`flex h-[36px] items-center justify-center gap-1 rounded-[5px] border text-[13px] font-bold ${selected
				? selectedClass
				: `${selectedClass} ${colorClass[color]} cursor-pointer`
				}`}
			onClick={() => onClick?.()}
		>
			<Icon size={14} />
			{label}
		</button>
	);
}

function TimeInput({ label, value, setTime, readOnly = false }) {
	return (
		<div>
			<Label>{label}</Label>
			<SmallTime value={value} setTime={setTime} readOnly={readOnly} />
		</div>
	);
}

function SmallTime({ value, setTime, readOnly = false }) {
	return (
		<div className="relative">
			<input
				type="time"
				value={value}
				readOnly={readOnly}
				onChange={(e) => setTime(e.target.value)}
				className="h-[36px] w-full rounded-[5px] border border-[#D1D5DB] !px-3 text-[13px] font-bold outline-none"
			/>
			{/* <Clock
				size={14}
				className="absolute right-3 top-1/2 -translate-y-1/2 text-[#9CA3AF]"
			/> */}
		</div>
	);
}

function Th({ children }) {
	return <th className="font-bold">{children}</th>;
}

function Td({ children, bold, color }) {
	const colorMap = {
		orange: 'text-[#EA580C] font-bold',
		green: 'text-[#16A34A] font-bold',
		sky: 'text-[#0284C7] font-bold',
		purple: 'text-[#8B5CF6] font-bold',
	};

	return (
		<td
			className={`${bold ? 'font-bold text-[#111827]' : 'text-[#4B5563]'} ${colorMap[color] || ''}`}
		>
			{children}
		</td>
	);
}

function StatusBadge({ type }) {
	const map = {
		출근: 'bg-[#DBEAFE] text-[#2563EB]',
		지각: 'bg-[#FFEDD5] text-[#EA580C]',
		연차: 'bg-[#DCFCE7] text-[#16A34A]',
		출장: 'bg-[#F3E8FF] text-[#8B5CF6]',
		반차: 'bg-[#E0F2FE] text-[#0284C7]',
		미등록: 'bg-[#FEF9C3] text-[#CA8A04]',
	};

	return (
		<span
			className={`rounded-full px-3 !py-1 text-[12px] font-bold ${map[type]}`}
		>
			● {type}
		</span>
	);
}

function PageBtn({ children, active }) {
	return (
		<button
			className={`flex h-[30px] w-[30px] items-center justify-center rounded-[5px] border text-[13px] font-bold ${active
				? 'border-[#183A6B] bg-[#183A6B] text-white'
				: 'border-[#E5E7EB] bg-white text-[#6B7280]'
				}`}
		>
			{children}
		</button>
	);
}
