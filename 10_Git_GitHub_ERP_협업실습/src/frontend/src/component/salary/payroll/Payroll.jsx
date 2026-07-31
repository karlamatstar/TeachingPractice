'use client';

import SalaryStatementModal from '@/component/modal/SalaryStatementModal';
import {
	TrendingUp,
	TrendingDown,
	WalletCards,
	Clock,
	CalendarDays,
	ChevronLeft,
	ChevronRight,
	ChevronDown,
	Search,
	RotateCcw,
	Table2,
} from 'lucide-react';

const rows = [
	[
		'EMP-001',
		'김철수',
		'인사팀',
		'4,200,000',
		'200,000',
		'150,000',
		'250,000',
		'4,800,000',
		'189,000',
		'167,400',
		'43,200',
		'132,000',
		'531,600',
		'4,268,400',
	],
	[
		'EMP-002',
		'이영희',
		'인사팀',
		'4,700,000',
		'200,000',
		'150,000',
		'120,000',
		'5,170,000',
		'211,500',
		'187,200',
		'46,530',
		'198,000',
		'643,230',
		'4,526,770',
	],
	[
		'EMP-003',
		'박민준',
		'개발팀',
		'3,500,000',
		'200,000',
		'150,000',
		'350,000',
		'4,200,000',
		'157,500',
		'139,300',
		'37,800',
		'88,000',
		'422,600',
		'3,777,400',
	],
	[
		'EMP-004',
		'최지영',
		'영업팀',
		'2,800,000',
		'200,000',
		'100,000',
		'-',
		'3,100,000',
		'126,000',
		'111,400',
		'27,900',
		'44,000',
		'309,300',
		'2,790,700',
	],
	[
		'EMP-005',
		'정수빈',
		'개발팀',
		'2,900,000',
		'200,000',
		'100,000',
		'180,000',
		'3,380,000',
		'130,500',
		'115,200',
		'30,420',
		'55,000',
		'331,120',
		'3,048,880',
	],
	[
		'EMP-006',
		'한지민',
		'영업팀',
		'3,200,000',
		'200,000',
		'100,000',
		'90,000',
		'3,590,000',
		'144,000',
		'127,300',
		'32,310',
		'77,000',
		'380,610',
		'3,209,390',
	],
];

export default function Payroll() {
	return (
		<main className="w-[1190px] bg-[#F3F6FA] p-[10px] text-[#1F2937]">
			<div className="grid grid-cols-4 gap-3">
				<Summary
					dark
					icon={<TrendingUp size={14} />}
					title="지급합계"
					value="28,640,000원"
					desc="전월 대비 +240,000원"
				/>
				<Summary
					icon={<TrendingDown size={14} />}
					title="공제합계"
					value="4,128,000원"
					desc="전월 대비 +34,000원"
					red
				/>
				<Summary
					green
					icon={<WalletCards size={14} />}
					title="실지급합계"
					value="24,512,000원"
					desc="대상인원 8명"
				/>
				<Summary
					yellow
					icon={<Clock size={14} />}
					title="지급상태"
					value="미확정 8건   확정 0건"
					desc="2025년 7월분"
				/>
			</div>

			<section className="mt-4 flex h-[60px] items-center justify-between rounded-[7px] border border-[#E5E7EB] bg-white px-5">
				<div className="flex items-center gap-4">
					<div className="flex h-[34px] overflow-hidden rounded-[5px] border border-[#D1D5DB]">
						<button className="w-[34px] bg-[#F8FAFC]">
							<ChevronLeft size={16} className="mx-auto" />
						</button>
						<div className="flex w-[160px] items-center justify-center gap-2 border-x text-[14px] font-bold">
							<CalendarDays size={15} className="text-[#183A6B]" />
							2025년 7월
						</div>
						<button className="w-[34px] bg-[#F8FAFC]">
							<ChevronRight size={16} className="mx-auto" />
						</button>
					</div>

					<Filter label="부서" value="전체 부서" />

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

					<button className="flex h-[34px] w-[82px] items-center justify-center gap-1 rounded-[5px] bg-[#183A6B] text-[13px] font-bold text-white">
						<Search size={14} />
						조회
					</button>

					<button className="flex h-[34px] w-[82px] items-center justify-center gap-1 rounded-[5px] border border-[#D1D5DB] bg-white text-[13px] font-bold text-[#6B7280]">
						<RotateCcw size={14} />
						초기화
					</button>
				</div>

				<div className="flex items-center gap-3 text-[12px] text-[#94A3B8]">
					<Legend color="bg-[#DBEAFE]" text="지급항목" />
					<Legend color="bg-[#FEE2E2]" text="공제항목" />
					<Legend color="bg-[#DCFCE7]" text="실지급" />
				</div>
			</section>

			<section className="mt-4 overflow-hidden rounded-[7px] border border-[#E5E7EB] bg-white">
				<div className="flex h-[44px] items-center justify-between bg-[#F8FAFC] px-5">
					<div className="flex items-center gap-2 text-[15px] font-bold text-[#183A6B]">
						<Table2 size={16} />
						2025년 7월 급여 지급 내역
					</div>

					<div className="flex items-center gap-2">
						<span className="rounded-full bg-[#DBEAFE] px-3 py-1 text-[12px] font-bold text-[#2563EB]">
							총 8명
						</span>
						<button className="h-[30px] rounded-[5px] border border-[#D1D5DB] bg-white px-3 text-[12px] text-[#4B5563]">
							☐ 전체선택
						</button>
					</div>
				</div>

				<table className="w-full table-fixed border-collapse text-center text-[13px]">
					<thead>
						<tr className="h-[40px] bg-[#F1F5F9] text-[#64748B]">
							<th className="w-[36px] border border-[#E5E7EB]">
								<input type="checkbox" defaultChecked />
							</th>
							<Th w="80px">사원번호</Th>
							<Th w="70px">성명</Th>
							<Th w="80px">부서</Th>
							<Th blue w="90px">
								기본급
							</Th>
							<Th blue w="75px">
								식대
							</Th>
							<Th blue w="75px">
								교통비
							</Th>
							<Th blue w="80px">
								야근수당
							</Th>
							<Th blue w="90px">
								지급소계
							</Th>
							<Th red w="80px">
								국민연금
							</Th>
							<Th red w="80px">
								건강보험
							</Th>
							<Th red w="80px">
								고용보험
							</Th>
							<Th red w="80px">
								소득세
							</Th>
							<Th red w="85px">
								공제소계
							</Th>
							<Th green w="125px">
								실지급액
							</Th>
						</tr>
					</thead>

					<tbody>
						{rows.map((r) => (
							<tr key={r[0]} className="h-[42px] bg-white">
								<td className="border border-[#E5E7EB]">
									<input type="checkbox" />
								</td>
								<Td>{r[0]}</Td>
								<Td bold>{r[1]}</Td>
								<Td>{r[2]}</Td>
								<Td blue bold>
									{r[3]}
								</Td>
								<Td blue>{r[4]}</Td>
								<Td blue>{r[5]}</Td>
								<Td blue>{r[6]}</Td>
								<Td blue bold>
									{r[7]}
								</Td>
								<Td red>{r[8]}</Td>
								<Td red>{r[9]}</Td>
								<Td red>{r[10]}</Td>
								<Td red>{r[11]}</Td>
								<Td red bold>
									{r[12]}
								</Td>
								<Td green bold large>
									{r[13]}
								</Td>
							</tr>
						))}
					</tbody>

					<tfoot>
						<tr className="h-[46px] bg-[#EAF2FF] font-bold">
							<td
								colSpan={4}
								className="border border-[#BFDBFE] text-right pr-5 text-[#183A6B]"
							>
								Σ 합계 (8명)
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								25,760,000
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								1,600,000
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								1,000,000
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								1,280,000
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								28,640,000
							</td>
							<td className="border border-[#FECACA] text-[#991B1B]">
								1,152,000
							</td>
							<td className="border border-[#FECACA] text-[#991B1B]">
								1,018,800
							</td>
							<td className="border border-[#FECACA] text-[#991B1B]">
								277,260
							</td>
							<td className="border border-[#FECACA] text-[#991B1B]">
								720,000
							</td>
							<td className="border border-[#FECACA] bg-[#FECACA] text-[#991B1B]">
								4,128,060
							</td>
							<td className="border border-[#BBF7D0] bg-[#DCFCE7] text-[#15803D]">
								24,511,940
							</td>
						</tr>
					</tfoot>
				</table>

				<div className="flex h-[44px] items-center justify-between px-5">
					<div className="flex items-center gap-3 text-[13px] text-[#64748B]">
						<span>총 8명 · 2025년 7월분 급여</span>
						<span className="rounded-full bg-[#FEF3C7] px-3 py-1 text-[12px] font-bold text-[#D97706]">
							ⓘ 미확정 8건 — 급여확정 후 명세서 발송 가능
						</span>
					</div>

					<div className="flex gap-1">
						<PageBtn>
							<ChevronLeft size={14} />
						</PageBtn>
						<PageBtn active>1</PageBtn>
						<PageBtn>2</PageBtn>
						<PageBtn>
							<ChevronRight size={14} />
						</PageBtn>
					</div>
				</div>
			</section>

			<SalaryStatementModal />
		</main>
	);
}

function Summary({ icon, title, value, desc, dark, red, green, yellow }) {
	let box = 'bg-white border-[#E5E7EB]';
	let titleCls = 'text-[#94A3B8]';
	let valueCls = 'text-[#111827]';
	let descCls = 'text-[#94A3B8]';

	if (dark) {
		box = 'bg-[#1E4E89] border-[#1E4E89] shadow';
		titleCls = 'text-[#A9C4E8]';
		valueCls = 'text-white';
		descCls = 'text-[#93C5FD]';
	} else if (red) {
		valueCls = 'text-[#111827]';
		titleCls = 'text-[#E11D48]';
		descCls = 'text-[#E11D48]';
	} else if (green) {
		box = 'bg-[#F0FDF4] border-[#BBF7D0]';
		titleCls = 'text-[#16A34A]';
		valueCls = 'text-[#15803D]';
		descCls = 'text-[#16A34A]';
	} else if (yellow) {
		box = 'bg-[#FFFBEB] border-[#FACC15]';
		titleCls = 'text-[#D97706]';
		valueCls = 'text-[#D97706]';
		descCls = 'text-[#94A3B8]';
	}

	return (
		<div
			className={`flex h-[82px] flex-col items-center justify-center rounded-[7px] border ${box}`}
		>
			<div
				className={`flex items-center gap-1 text-[13px] font-bold ${titleCls}`}
			>
				{icon}
				{title}
			</div>

			{yellow ? (
				<div className="mt-2 flex gap-2 text-[12px] font-bold">
					<span className="rounded-full bg-[#FEF3C7] px-3 py-1 text-[#D97706]">
						미확정 8건
					</span>
					<span className="rounded-full bg-[#DCFCE7] px-3 py-1 text-[#16A34A]">
						확정 0건
					</span>
				</div>
			) : (
				<p className={`mt-1 text-[22px] font-extrabold ${valueCls}`}>{value}</p>
			)}

			<p className={`mt-1 text-[12px] font-bold ${descCls}`}>{desc}</p>
		</div>
	);
}

function Filter({ label, value }) {
	return (
		<div className="flex items-center gap-2">
			<span className="text-[14px] font-bold">{label}</span>
			<button className="flex h-[34px] w-[150px] items-center justify-between rounded-[5px] border border-[#D1D5DB] px-3 text-[13px] text-[#6B7280]">
				{value}
				<ChevronDown size={14} className="text-[#9CA3AF]" />
			</button>
		</div>
	);
}

function Legend({ color, text }) {
	return (
		<span className="flex items-center gap-1">
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

function Td({ children, bold, blue, red, green, large }) {
	return (
		<td
			className={`border border-[#E5E7EB] ${
				bold ? 'font-bold text-[#111827]' : 'text-[#4B5563]'
			} ${blue ? 'bg-[#EFF6FF] text-[#2563EB]' : ''} ${
				red ? 'bg-[#FEF2F2] text-[#EF4444]' : ''
			} ${green ? 'bg-[#DCFCE7] text-[#15803D]' : ''} ${
				large ? 'text-[15px]' : ''
			}`}
		>
			{children}
		</td>
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
