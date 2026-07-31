'use client';

import {
	CalendarDays,
	ChevronLeft,
	ChevronRight,
	RotateCcw,
	Table2,
	RefreshCw,
	Calculator,
	Check,
	Users,
	TrendingUp,
	TrendingDown,
	WalletCards,
	Clock,
	SlidersHorizontal,
} from 'lucide-react';

const rows = [
	[
		'EMP-001',
		'김철수',
		'인사팀',
		'4,200,000',
		'600,000',
		'4,800,000',
		'399,600',
		'145,200',
		'544,800',
		'4,255,200',
		'계산전',
	],
	[
		'EMP-002',
		'이영희',
		'인사팀',
		'4,700,000',
		'470,000',
		'5,170,000',
		'445,230',
		'217,800',
		'663,030',
		'4,506,970',
		'계산전',
	],
	[
		'EMP-003',
		'박민준',
		'개발팀',
		'3,500,000',
		'500,000',
		'4,000,000',
		'344,400',
		'96,800',
		'441,200',
		'3,558,800',
		'검토필요',
	],
	[
		'EMP-004',
		'최지영',
		'영업팀',
		'2,800,000',
		'300,000',
		'3,100,000',
		'266,940',
		'48,400',
		'315,340',
		'2,784,660',
		'계산전',
	],
	[
		'EMP-005',
		'정수빈',
		'개발팀',
		'2,900,000',
		'480,000',
		'3,380,000',
		'290,952',
		'60,500',
		'351,452',
		'3,028,548',
		'계산전',
	],
];

export default function SalaryCalculation() {
	return (
		<main className="w-[1190px] bg-[#F3F6FA] p-[10px] text-[#1F2937]">
			<div className="grid grid-cols-[420px_1fr] gap-3">
				<section className="rounded-[8px] border bg-white p-5">
					<div className="grid grid-cols-[220px_1fr_1fr] gap-4">
						<div>
							<p className="mb-1 text-[12px] font-bold text-[#94A3B8]">
								계산기준월
							</p>
							<div className="flex h-[36px] overflow-hidden rounded-[5px] border">
								<button className="w-[36px] bg-[#F8FAFC]">
									<ChevronLeft size={15} className="mx-auto" />
								</button>
								<div className="flex flex-1 items-center justify-center gap-2 border-x text-[17px] font-bold">
									<CalendarDays size={16} className="text-[#183A6B]" /> 2025년
									7월
								</div>
								<button className="w-[36px] bg-[#F8FAFC]">
									<ChevronRight size={15} className="mx-auto" />
								</button>
							</div>
						</div>

						<StatusMini title="계산상태" text="계산전" color="yellow" />
						<StatusMini title="확정상태" text="미확정" color="gray" />
					</div>
				</section>

				<section className="rounded-[8px] border bg-white">
					<div className="flex h-[44px] items-center justify-between border-b px-5">
						<div className="flex items-center gap-2 text-[15px] font-bold text-[#183A6B]">
							<SlidersHorizontal size={16} /> 계산조건 설정
						</div>
						<button className="flex h-[30px] items-center gap-1 rounded-[6px] bg-[#F8FAFC] px-3 text-[12px] font-bold text-[#64748B]">
							<RotateCcw size={14} /> 기본값
						</button>
					</div>

					<div className="grid grid-cols-4 px-5 py-4">
						<SwitchItem
							title="근태 데이터 연동"
							desc="야근 · 지각 데이터 자동 반영"
							on
						/>
						<SwitchItem
							title="간이세액표 적용"
							desc="국세청 간이세액 기준 소득세 계산"
							on
						/>
						<SwitchItem title="원 단위 반올림" desc="1원 미만 반올림 처리" />
						<SwitchItem
							title="지방소득세 자동포함"
							desc="소득세의 10% 자동 산출"
							on
						/>
					</div>
				</section>
			</div>

			<div className="mt-4 grid grid-cols-5 gap-3">
				<Summary
					dark
					icon={<TrendingUp size={14} />}
					title="지급합계"
					value="28,640,000원"
					desc="기본급 25,760,000 + 수당 2,880,000"
				/>
				<Summary
					icon={<TrendingDown size={14} />}
					title="공제합계"
					value="4,128,060원"
					desc="4대보험 3,408,060 + 소득세 720,000"
					red
				/>
				<Summary
					green
					icon={<WalletCards size={14} />}
					title="실지급합계"
					value="24,511,940원"
					desc="1인 평균 3,063,993원"
				/>
				<Summary
					blue
					icon={<Users size={14} />}
					title="계산 대상"
					value="8명"
					badge="계산전 8명"
				/>
				<Summary
					yellow
					icon={<Clock size={14} />}
					title="전월 대비"
					value="+206,000원"
					desc="야근수당 증가 영향"
				/>
			</div>

			<section className="mt-4 overflow-hidden rounded-[8px] border bg-white">
				<div className="flex h-[44px] items-center justify-between bg-[#F8FAFC] px-5">
					<div className="flex items-center gap-2 text-[16px] font-bold text-[#183A6B]">
						<Table2 size={17} /> 2025년 7월 급여계산 미리보기
					</div>

					<div className="flex items-center gap-3 text-[12px]">
						<span className="rounded-full bg-[#DBEAFE] px-3 py-1 font-bold text-[#2563EB]">
							총 8명
						</span>
						<Legend color="bg-[#DBEAFE]" text="지급" />
						<Legend color="bg-[#FEE2E2]" text="공제" />
						<Legend color="bg-[#DCFCE7]" text="실지급" />
						<button className="flex h-[30px] items-center gap-1 rounded-[5px] border border-[#BFDBFE] bg-[#EFF6FF] px-3 font-bold text-[#2563EB]">
							<RefreshCw size={14} /> 재계산
						</button>
					</div>
				</div>

				<table className="w-full table-fixed border-collapse text-center text-[13px]">
					<thead>
						<tr className="h-[40px] bg-[#F1F5F9] text-[#64748B]">
							<Th w="80px">사원번호</Th>
							<Th w="70px">성명</Th>
							<Th w="80px">부서</Th>
							<Th blue w="95px">
								기본급
							</Th>
							<Th blue w="90px">
								수당합계
							</Th>
							<Th blue w="95px">
								지급소계
							</Th>
							<Th red w="95px">
								4대보험
							</Th>
							<Th red w="95px">
								소득세+지방
							</Th>
							<Th red w="95px">
								공제소계
							</Th>
							<Th green w="360px">
								실지급액
							</Th>
							<Th w="80px">상태</Th>
						</tr>
					</thead>

					<tbody>
						{rows.map((r) => (
							<tr
								key={r[0]}
								className={`h-[42px] ${r[0] === 'EMP-003' ? 'bg-[#FFFBEB]' : 'bg-white'}`}
							>
								<Td>{r[0]}</Td>
								<Td bold>
									{r[1]}{' '}
									{r[0] === 'EMP-003' && (
										<span className="text-[#F59E0B]">ⓘ</span>
									)}
								</Td>
								<Td>{r[2]}</Td>
								<Td blue bold>
									{r[3]}
								</Td>
								<Td blue bold={r[0] === 'EMP-003'} orange={r[0] === 'EMP-003'}>
									{r[4]}
								</Td>
								<Td blue bold>
									{r[5]}
								</Td>
								<Td red>{r[6]}</Td>
								<Td red>{r[7]}</Td>
								<Td red bold>
									{r[8]}
								</Td>
								<Td green bold large>
									{r[9]}
								</Td>
								<td className="border border-[#E5E7EB]">
									<StatusBadge status={r[10]} />
								</td>
							</tr>
						))}
					</tbody>

					<tfoot>
						<tr className="h-[46px] bg-[#EAF2FF] font-bold">
							<td
								colSpan={3}
								className="border border-[#BFDBFE] text-right pr-5 text-[#183A6B]"
							>
								Σ 합계 (8명)
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								25,760,000
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								2,880,000
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								28,640,000
							</td>
							<td className="border border-[#FECACA] text-[#991B1B]">
								3,408,060
							</td>
							<td className="border border-[#FECACA] text-[#991B1B]">
								720,000
							</td>
							<td className="border border-[#FECACA] text-[#991B1B]">
								4,128,060
							</td>
							<td className="border border-[#BBF7D0] bg-[#DCFCE7] text-[16px] text-[#15803D]">
								24,511,940
							</td>
							<td className="border border-[#BFDBFE] text-[#64748B]">-</td>
						</tr>
					</tfoot>
				</table>

				<div className="flex h-[46px] items-center justify-between px-5">
					<div className="flex items-center gap-3 text-[13px] text-[#64748B]">
						<span>총 8명 · 검토필요 1명</span>
						<span className="text-[#CBD5E1]">|</span>
						<span className="font-bold text-[#EA580C]">
							ⓘ EMP-003 박민준 · 야근수당 데이터 불일치 — 확인 필요
						</span>
					</div>

					<div className="flex items-center gap-2">
						<PageBtn>
							<ChevronLeft size={14} />
						</PageBtn>
						<PageBtn active>1</PageBtn>
						<PageBtn>
							<ChevronRight size={14} />
						</PageBtn>

						<button className="ml-2 flex h-[36px] items-center gap-2 rounded-[5px] bg-[#2563EB] px-5 text-[14px] font-bold text-white">
							<Calculator size={15} /> 전직원 일괄계산
						</button>
						<button className="flex h-[36px] items-center gap-2 rounded-[5px] bg-[#183A6B] px-5 text-[14px] font-bold text-white">
							<Check size={16} /> 급여확정
						</button>
					</div>
				</div>
			</section>
		</main>
	);
}

function StatusMini({ title, text, color }) {
	const cls =
		color === 'yellow'
			? 'bg-[#FEF3C7] text-[#CA8A04]'
			: 'bg-[#F1F5F9] text-[#64748B]';

	return (
		<div>
			<p className="mb-1 text-[12px] font-bold text-[#94A3B8]">{title}</p>
			<span
				className={`inline-flex h-[30px] items-center rounded-full px-4 text-[13px] font-bold ${cls}`}
			>
				● {text}
			</span>
		</div>
	);
}

function SwitchItem({ title, desc, on }) {
	return (
		<div>
			<div className="flex items-center gap-3">
				<div>
					<p className="text-[14px] font-bold">{title}</p>
					<p className="mt-1 text-[11px] text-[#94A3B8]">{desc}</p>
				</div>
				<span
					className={`ml-auto h-5 w-10 rounded-full p-[2px] ${on ? 'bg-[#183A6B]' : 'bg-[#CBD5E1]'}`}
				>
					<span
						className={`block h-4 w-4 rounded-full bg-white ${on ? 'translate-x-5' : ''}`}
					/>
				</span>
			</div>
		</div>
	);
}

function Summary({
	icon,
	title,
	value,
	desc,
	badge,
	dark,
	red,
	green,
	blue,
	yellow,
}) {
	let box = 'bg-white border-[#E5E7EB]';
	let titleCls = 'text-[#94A3B8]';
	let valueCls = 'text-[#111827]';
	let descCls = 'text-[#94A3B8]';

	if (dark) {
		box = 'bg-[#1E4E89] border-[#1E4E89]';
		titleCls = 'text-[#93C5FD]';
		valueCls = 'text-white';
		descCls = 'text-[#93C5FD]';
	} else if (red) {
		titleCls = 'text-[#E11D48]';
		descCls = 'text-[#E11D48]';
	} else if (green) {
		box = 'bg-[#F0FDF4] border-[#BBF7D0]';
		titleCls = 'text-[#16A34A]';
		valueCls = 'text-[#15803D]';
		descCls = 'text-[#16A34A]';
	} else if (blue) {
		box = 'bg-[#EFF6FF] border-[#BFDBFE]';
		titleCls = 'text-[#2563EB]';
		valueCls = 'text-[#2563EB]';
	} else if (yellow) {
		box = 'bg-[#FFFBEB] border-[#FACC15]';
		titleCls = 'text-[#D97706]';
		valueCls = 'text-[#B45309]';
		descCls = 'text-[#EA580C]';
	}

	return (
		<div
			className={`flex h-[78px] flex-col items-center justify-center rounded-[7px] border ${box}`}
		>
			<p
				className={`flex items-center gap-1 text-[13px] font-bold ${titleCls}`}
			>
				{icon}
				{title}
			</p>
			<p className={`mt-1 text-[23px] font-extrabold ${valueCls}`}>{value}</p>
			{badge && (
				<span className="rounded-full bg-[#FEF3C7] px-3 py-[2px] text-[11px] font-bold text-[#CA8A04]">
					{badge}
				</span>
			)}
			{desc && (
				<p className={`mt-1 text-[12px] font-bold ${descCls}`}>{desc}</p>
			)}
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

function Th({ children, w, blue, red, green }) {
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

function Td({ children, bold, blue, red, green, orange, large }) {
	return (
		<td
			className={`border border-[#E5E7EB] ${
				bold ? 'font-bold text-[#111827]' : 'text-[#4B5563]'
			} ${blue ? 'bg-[#EFF6FF] text-[#2563EB]' : ''} ${
				red ? 'bg-[#FEF2F2] text-[#EF4444]' : ''
			} ${green ? 'bg-[#DCFCE7] text-[#15803D]' : ''} ${
				orange ? 'text-[#F59E0B]' : ''
			} ${large ? 'text-[15px]' : ''}`}
		>
			{children}
		</td>
	);
}

function StatusBadge({ status }) {
	const cls =
		status === '검토필요'
			? 'bg-[#FFE4E6] text-[#E11D48]'
			: 'bg-[#FEF3C7] text-[#CA8A04]';

	return (
		<span className={`rounded-full px-3 py-1 text-[12px] font-bold ${cls}`}>
			{status}
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
