'use client';

import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog';
import { IdCard, Printer, X, User, Upload, Clock } from 'lucide-react';

const appointmentRows = [
	{
		date: '2025.07.01',
		type: '승진',
		typeColor: 'green',
		before: '경영지원팀 · 과장',
		after: '인사팀 · 차장',
		no: 'APT-2025-003',
	},
	{
		date: '2022.01.03',
		type: '전보',
		typeColor: 'yellow',
		before: '총무팀 · 대리',
		after: '경영지원팀 · 과장',
		no: 'APT-2022-001',
	},
	{
		date: '2018.07.15',
		type: '신규입사',
		typeColor: 'purple',
		before: '-',
		after: '총무팀 · 사원',
		no: 'APT-2018-012',
	},
];

export default function PersonnelRecordModal({ open, setOpen }) {
	return (
		<Dialog open={open} onOpenChange={setOpen}>
			<DialogContent className="w-[700px] max-w-[700px] overflow-hidden rounded-[10px] border-0 p-0">
				{/* Header */}
				<div className="flex h-[60px] items-center justify-between bg-[#1F4478] px-5 text-white">
					<div className="flex items-center gap-3">
						<IdCard size={18} className="text-[#93C5FD]" />
						<DialogTitle className="text-[20px] font-bold">
							인사기록카드
						</DialogTitle>
						<span className="rounded-full bg-[#3B6CA8] px-4 py-1 text-[13px] font-bold text-[#BFDBFE]">
							2025년 기준
						</span>
					</div>

					<div className="flex items-center gap-2">
						<button className="flex h-9 items-center gap-2 rounded-[6px] bg-[#3569A5] px-4 text-[14px] font-bold text-[#BFDBFE]">
							<Printer size={15} />
							인쇄
						</button>
						<button
							onClick={() => setOpen(false)}
							className="flex h-9 w-9 items-center justify-center rounded-[6px] bg-[#3569A5]"
						>
							<X size={20} />
						</button>
					</div>
				</div>

				{/* Profile */}
				<div className="grid grid-cols-[100px_1fr] gap-5 bg-[#F8FAFC] px-5 py-4">
					<div className="flex flex-col items-center">
						<div className="flex h-[88px] w-[76px] flex-col items-center justify-center rounded-[8px] border border-[#CBD5E1] bg-[#E2E8F0] text-[#94A3B8]">
							<User size={32} />
							<span className="mt-1 text-[13px]">사진</span>
						</div>
						<button className="mt-2 flex h-[26px] items-center gap-1 rounded-[4px] border bg-white px-3 text-[12px] text-[#64748B]">
							<Upload size={12} />
							변경
						</button>
					</div>

					<div className="grid grid-cols-4 gap-y-3 text-[14px]">
						<Info title="사원번호" value="EMP-002" />
						<Info title="성명" value="이영희" />
						<Info title="생년월일" value="1988.05.14" />
						<Info title="성별" value="여" />

						<Info title="부서" value="인사팀" blue />
						<Info title="직급" value="차장" />
						<Info title="입사일" value="2018.07.15" />
						<Info title="재직상태" value="재직중" badge />

						<Info title="휴대폰" value="010-9876-5432" />
						<Info title="이메일" value="lee@company.com" wide />
						<Info title="근속연수" value="6년 11개월" blue />
					</div>
				</div>

				{/* Tabs */}
				<div className="flex h-[46px] items-center border-y bg-white px-5">
					{['발령이력', '근태요약', '급여이력', '자격증/학력'].map(
						(tab, idx) => (
							<button
								key={tab}
								className={`h-full px-5 text-[14px] font-bold ${
									idx === 0
										? 'border-b-2 border-[#1F4478] text-[#1F4478]'
										: 'text-[#9CA3AF]'
								}`}
							>
								{tab}
							</button>
						)
					)}
					<div className="ml-auto h-px flex-1 bg-[#E5E7EB]" />
				</div>

				{/* Content */}
				<div className="bg-white px-5 py-4">
					<div className="mb-3 flex items-center justify-between">
						<h3 className="border-l-4 border-[#1F4478] pl-2 text-[16px] font-bold text-[#1F4478]">
							발령 이력
						</h3>
						<span className="rounded-full bg-[#EFF6FF] px-3 py-1 text-[12px] font-bold text-[#2563EB]">
							총 3건
						</span>
					</div>

					<table className="w-full table-fixed border-collapse text-center text-[14px]">
						<thead>
							<tr className="h-[38px] bg-[#F1F5F9] text-[#64748B]">
								<th>발령일</th>
								<th>발령유형</th>
								<th>발령전 부서/직급</th>
								<th>발령후 부서/직급</th>
								<th>발령번호</th>
							</tr>
						</thead>

						<tbody>
							{appointmentRows.map((row) => (
								<tr key={row.no} className="h-[42px] border-b">
									<td className="text-[#374151]">{row.date}</td>
									<td>
										<StatusBadge text={row.type} color={row.typeColor} />
									</td>
									<td className="text-[#9CA3AF]">{row.before}</td>
									<td className="font-bold text-[#2563EB]">{row.after}</td>
									<td className="text-[#374151]">{row.no}</td>
								</tr>
							))}
						</tbody>
					</table>
				</div>

				{/* Footer */}
				<div className="flex h-[58px] items-center justify-between border-t bg-[#F8FAFC] px-5">
					<div className="flex items-center gap-1 text-[13px] text-[#9CA3AF]">
						<Clock size={14} />
						최종 수정: 2025.07.01 · 홍길동 (인사팀)
					</div>

					<button
						onClick={() => setOpen(false)}
						className="flex h-[38px] w-[92px] items-center justify-center gap-2 rounded-[6px] bg-[#1F4478] text-[14px] font-bold text-white"
					>
						<X size={16} />
						닫기
					</button>
				</div>
			</DialogContent>
		</Dialog>
	);
}

function Info({ title, value, blue, badge, wide }) {
	return (
		<div className={wide ? 'col-span-2 border-l pl-4' : 'border-l pl-4'}>
			<p className="text-[12px] font-bold text-[#9CA3AF]">{title}</p>
			{badge ? (
				<span className="mt-1 inline-flex rounded-full bg-[#DCFCE7] px-3 py-1 text-[12px] font-bold text-[#16A34A]">
					{value}
				</span>
			) : (
				<p
					className={`mt-1 text-[14px] font-bold ${
						blue ? 'text-[#2563EB]' : 'text-[#111827]'
					}`}
				>
					{value}
				</p>
			)}
		</div>
	);
}

function StatusBadge({ text, color }) {
	const map = {
		green: 'bg-[#DCFCE7] text-[#16A34A]',
		yellow: 'bg-[#FEF3C7] text-[#CA8A04]',
		purple: 'bg-[#F3E8FF] text-[#8B5CF6]',
	};

	return (
		<span
			className={`rounded-full px-3 py-1 text-[12px] font-bold ${map[color]}`}
		>
			{text}
		</span>
	);
}
