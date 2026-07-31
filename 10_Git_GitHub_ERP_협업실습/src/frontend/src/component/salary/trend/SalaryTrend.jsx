'use client';

import {
	BarChart3,
	CalendarDays,
	ChevronLeft,
	ChevronRight,
	FileText,
	Lock,
	Table2,
} from 'lucide-react';

const historyRows = [
	[
		'이번달\n2025년 7월',
		'3,500,000',
		'500,000',
		'4,000,000',
		'441,200',
		'3,558,800',
		'2025.07.25',
		'미확정',
		'미리보기',
	],
	[
		'2025년 6월',
		'3,500,000',
		'350,000',
		'3,850,000',
		'431,400',
		'3,418,600',
		'2025.06.25',
		'확정',
		'명세서',
	],
	[
		'2025년 5월',
		'3,500,000',
		'380,000',
		'3,880,000',
		'434,640',
		'3,445,360',
		'2025.05.25',
		'확정',
		'명세서',
	],
	[
		'2025년 4월',
		'3,500,000',
		'350,000',
		'3,850,000',
		'431,400',
		'3,418,600',
		'2025.04.25',
		'확정',
		'명세서',
	],
	[
		'2025년 3월',
		'3,500,000',
		'350,000',
		'3,850,000',
		'431,400',
		'3,418,600',
		'2025.03.25',
		'확정',
		'명세서',
	],
];

export default function SalaryTrend() {
	return (
		<main className="w-[1190px] bg-[#F3F6FA] p-[10px] text-[#1F2937]">
			<section className="overflow-hidden rounded-[7px] border bg-white">
				<div className="flex h-[44px] items-center justify-between border-b bg-[#F8FAFC] px-5">
					<div className="flex items-center gap-3">
						<div className="flex items-center gap-2 text-[15px] font-bold text-[#183A6B]">
							<BarChart3 size={16} />
							2025년 월별 실지급액 추이
						</div>
						<span className="rounded-full bg-[#EFF6FF] px-3 py-1 text-[12px] font-bold text-[#2563EB]">
							2025년
						</span>
					</div>

					<div className="flex gap-4 text-[12px] font-bold text-[#9CA3AF]">
						<span className="flex items-center gap-1">
							<b className="h-3 w-3 rounded-[3px] bg-[#183A6B]" /> 실지급액
						</span>
						<span className="flex items-center gap-1">
							<b className="h-3 w-3 rounded-[3px] bg-[#3B82F6]" /> 이번달 (7월)
						</span>
						<span className="flex items-center gap-1">
							<b className="h-3 w-3 rounded-[3px] bg-[#E2E8F0]" /> 미지급
						</span>
					</div>
				</div>

				<div className="grid grid-cols-[1fr_160px] gap-6 px-8 py-5">
					<Chart />

					<div className="flex flex-col justify-center gap-4">
						<SideStat blue title="2025년 누적" value="17,023,590" unit="원" />
						<SideStat
							green
							title="최고 지급월"
							value="5월"
							unit="2,490,000원"
						/>
						<SideStat title="월 평균" value="2,432,000" unit="원" />
					</div>
				</div>
			</section>

			<section className="mt-4 flex h-[60px] items-center justify-between rounded-[7px] border bg-white px-5">
				<div className="flex items-center gap-4">
					<span className="text-[14px] font-bold">조회년도</span>
					<div className="flex h-[34px] overflow-hidden rounded-[5px] border">
						<button className="w-[34px] bg-[#F8FAFC]">
							<ChevronLeft size={15} className="mx-auto" />
						</button>
						<div className="flex w-[110px] items-center justify-center gap-2 border-x text-[14px] font-bold">
							<CalendarDays size={15} className="text-[#183A6B]" />
							2025년
						</div>
						<button className="w-[34px] bg-[#F8FAFC]">
							<ChevronRight size={15} className="mx-auto" />
						</button>
					</div>

					<span className="text-[14px] font-bold">조회대상</span>
					<div className="flex h-[34px] w-[180px] items-center justify-between rounded-[5px] border px-3 text-[13px] font-bold">
						<span>
							<b className="mr-2 inline-flex h-6 w-6 items-center justify-center rounded-full bg-[#DBEAFE] text-[11px] text-[#2563EB]">
								박
							</b>
							박민준 (본인)
						</span>
						<Lock size={13} className="text-[#CBD5E1]" />
					</div>

					<span className="rounded-full bg-[#EFF6FF] px-4 py-2 text-[13px] font-bold text-[#2563EB]">
						개발팀 · 대리
					</span>
				</div>

				<div className="flex h-[34px] overflow-hidden rounded-[5px] border">
					{['2023', '2024', '2025'].map((year) => (
						<button
							key={year}
							className={`w-[54px] text-[13px] font-bold ${
								year === '2025'
									? 'bg-[#183A6B] text-white'
									: 'bg-white text-[#CBD5E1]'
							}`}
						>
							{year}
						</button>
					))}
				</div>
			</section>

			<section className="mt-4 overflow-hidden rounded-[7px] border bg-white">
				<div className="flex h-[44px] items-center justify-between bg-[#F8FAFC] px-5">
					<div className="flex items-center gap-2 text-[15px] font-bold text-[#183A6B]">
						<Table2 size={16} />
						2025년 월별 급여 수정 이력
					</div>

					<div className="flex items-center gap-3 text-[12px]">
						<span className="rounded-full bg-[#EFF6FF] px-3 py-1 font-bold text-[#2563EB]">
							7개월 조회
						</span>
						<Legend color="bg-[#DBEAFE]" text="지급" />
						<Legend color="bg-[#FEE2E2]" text="공제" />
						<Legend color="bg-[#DCFCE7]" text="실지급" />
					</div>
				</div>

				<table className="w-full table-fixed border-collapse text-center text-[13px]">
					<thead>
						<tr className="h-[40px] bg-[#F1F5F9] text-[#64748B]">
							<Th w="110px">지급연월</Th>
							<Th blue>기본급</Th>
							<Th blue>수당합계</Th>
							<Th blue>지급소계</Th>
							<Th red>공제합계</Th>
							<Th green>실지급액</Th>
							<Th w="100px">지급일</Th>
							<Th w="80px">상태</Th>
							<Th w="330px">명세서</Th>
						</tr>
					</thead>

					<tbody>
						{historyRows.map((r, idx) => (
							<tr
								key={idx}
								className={`h-[44px] ${idx === 0 ? 'bg-[#EFF6FF]' : 'bg-white'}`}
							>
								<Td first current={idx === 0}>
									{r[0].split('\n').map((v) => (
										<div key={v}>{v}</div>
									))}
								</Td>
								<Td blue bold>
									{r[1]}
								</Td>
								<Td blue>{r[2]}</Td>
								<Td blue bold>
									{r[3]}
								</Td>
								<Td red bold>
									{r[4]}
								</Td>
								<Td green bold large>
									{r[5]}
								</Td>
								<Td>{r[6]}</Td>
								<td className="border border-[#E5E7EB]">
									<StatusBadge status={r[7]} />
								</td>
								<td className="border border-[#E5E7EB]">
									<button
										className={`rounded-[5px] px-4 py-1 text-[13px] font-bold ${
											idx === 0
												? 'border border-[#BFDBFE] bg-white text-[#2563EB]'
												: 'bg-[#EFF6FF] text-[#2563EB]'
										}`}
									>
										<FileText size={13} className="mr-1 inline" />
										{r[8]}
									</button>
								</td>
							</tr>
						))}
					</tbody>

					<tfoot>
						<tr className="h-[44px] bg-[#EAF2FF] font-bold">
							<td className="border border-[#BFDBFE] text-[#183A6B]">
								Σ 7개월 합계
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								24,500,000
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								2,660,000
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								27,160,000
							</td>
							<td className="border border-[#FECACA] text-[#991B1B]">
								3,136,410
							</td>
							<td className="border border-[#BBF7D0] text-[#15803D]">
								24,023,590
							</td>
							<td className="border border-[#BFDBFE] text-[#94A3B8]">-</td>
							<td className="border border-[#BFDBFE] text-[#94A3B8]">-</td>
							<td className="border border-[#BFDBFE] text-[#94A3B8]">-</td>
						</tr>
					</tfoot>
				</table>

				<div className="flex h-[44px] items-center justify-between px-5">
					<div className="flex items-center gap-3 text-[13px] text-[#64748B]">
						<span>2025년 1~7월 표시 · 8~12월 미지급</span>
						<span className="rounded-full bg-[#EFF6FF] px-4 py-1 text-[12px] font-bold text-[#2563EB]">
							↗ 월평균 실지급 3,431,942원
						</span>
					</div>

					<div className="flex gap-1">
						<PageBtn>
							<ChevronLeft size={14} />
						</PageBtn>
						<PageBtn active>1</PageBtn>
						<PageBtn>
							<ChevronRight size={14} />
						</PageBtn>
					</div>
				</div>
			</section>
		</main>
	);
}

function Chart() {
	const bars = [
		[238, '1월', false],
		[241, '2월', false],
		[245, '3월', false],
		[243, '4월', false],
		[249, '5월', false],
		[245, '6월', false],
		[356, '7월', true],
		[40, '8월', null],
		[40, '9월', null],
		[40, '10월', null],
		[40, '11월', null],
		[40, '12월', null],
	];

	return (
		<div className="relative h-[270px] px-8 pt-8">
			<div className="absolute left-0 top-8 h-[170px] w-full">
				{[0, 1, 2, 3].map((i) => (
					<div
						key={i}
						className="absolute left-0 w-full border-t border-[#E5E7EB]"
						style={{ top: `${i * 56}px` }}
					/>
				))}
			</div>

			<div className="relative z-10 flex h-[210px] items-end gap-6">
				{bars.map(([value, month, active], idx) => (
					<div key={month} className="flex w-[45px] flex-col items-center">
						<div className="mb-1 text-[11px] font-bold text-[#94A3B8]">
							{active === null ? '' : value}
						</div>
						{active && (
							<span className="mb-1 rounded-[4px] bg-[#2563EB] px-3 py-1 text-[11px] font-bold text-white">
								이번달
							</span>
						)}
						<div
							className={`w-[34px] rounded-t-[5px] ${
								active === true
									? 'bg-[#2563EB]'
									: active === null
										? 'bg-[#E2E8F0]'
										: 'bg-[#526B8F]'
							}`}
							style={{ height: `${active === null ? 20 : value / 1.4}px` }}
						/>
						<span
							className={`mt-2 text-[12px] font-bold ${
								active ? 'text-[#183A6B]' : 'text-[#CBD5E1]'
							}`}
						>
							{month}
						</span>
					</div>
				))}
			</div>
		</div>
	);
}

function SideStat({ title, value, unit, blue, green }) {
	return (
		<div
			className={`flex h-[80px] flex-col items-center justify-center rounded-[7px] border ${
				blue
					? 'border-[#BFDBFE] bg-[#EFF6FF] text-[#2563EB]'
					: green
						? 'border-[#BBF7D0] bg-[#F0FDF4] text-[#16A34A]'
						: 'border-[#E5E7EB] bg-white text-[#374151]'
			}`}
		>
			<p className="text-[12px] font-bold">{title}</p>
			<p className="mt-1 text-[20px] font-extrabold">{value}</p>
			<p className="text-[12px] font-bold">{unit}</p>
		</div>
	);
}

function Legend({ color, text }) {
	return (
		<span className="flex items-center gap-1 text-[#94A3B8]">
			<b className={`h-2 w-2 rounded-full ${color}`} />
			{text}
		</span>
	);
}

function Th({ children, blue, red, green, w }) {
	return (
		<th
			style={{ width: w }}
			className={`border font-bold ${
				blue
					? 'border-[#BFDBFE] bg-[#EFF6FF] text-[#2563EB]'
					: red
						? 'border-[#FECACA] bg-[#FEF2F2] text-[#DC2626]'
						: green
							? 'border-[#BBF7D0] bg-[#DCFCE7] text-[#15803D]'
							: 'border-[#E5E7EB]'
			}`}
		>
			{children}
		</th>
	);
}

function Td({ children, blue, red, green, bold, large, first, current }) {
	return (
		<td
			className={`border border-[#E5E7EB] ${
				bold ? 'font-bold text-[#111827]' : 'text-[#4B5563]'
			} ${blue ? 'bg-[#EFF6FF] text-[#2563EB]' : ''} ${
				red ? 'bg-[#FEF2F2] text-[#EF4444]' : ''
			} ${green ? 'bg-[#DCFCE7] text-[#15803D]' : ''} ${
				first ? 'font-bold text-[#64748B]' : ''
			} ${current ? 'text-[#2563EB]' : ''} ${large ? 'text-[15px]' : ''}`}
		>
			{children}
		</td>
	);
}

function StatusBadge({ status }) {
	return (
		<span
			className={`rounded-full px-3 py-1 text-[12px] font-bold ${
				status === '미확정'
					? 'bg-[#FEF3C7] text-[#CA8A04]'
					: 'bg-[#DCFCE7] text-[#16A34A]'
			}`}
		>
			● {status}
		</span>
	);
}

function PageBtn({ children, active }) {
	return (
		<button
			className={`flex h-[30px] w-[30px] items-center justify-center rounded-[5px] border text-[13px] font-bold ${
				active
					? 'border-[#183A6B] bg-[#183A6B] text-white'
					: 'border-[#E5E7EB] bg-white text-[#64748B]'
			}`}
		>
			{children}
		</button>
	);
}
