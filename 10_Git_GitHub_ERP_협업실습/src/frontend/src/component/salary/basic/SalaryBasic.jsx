'use client';

import {
	Search,
	RotateCcw,
	CalendarDays,
	ChevronDown,
	ChevronLeft,
	ChevronRight,
	Table2,
	Pencil,
	Clock,
	Save,
	X,
} from 'lucide-react';

const rows = [
	{
		id: 'EMP-001',
		name: '김철수',
		dept: '인사팀',
		rank: '팀장',
		rankColor: 'purple',
		base: '4,200,000',
		meal: '200,000',
		traffic: '150,000',
		position: '200,000',
		allowance: '550,000',
		bank: '국민은행',
		account: '12****-34****',
		start: '2024.01.01',
		edit: false,
	},
	{
		id: 'EMP-002',
		name: '이영희',
		dept: '인사팀',
		rank: '차장',
		rankColor: 'blue',
		base: '4,700,000',
		meal: '200,000',
		traffic: '150,000',
		position: '200,000',
		allowance: '550,000',
		bank: '신한은행',
		account: '98****-12****',
		start: '2025.01.01',
		edit: false,
	},
	{
		id: 'EMP-003',
		name: '박민준',
		dept: '개발팀',
		rank: '대리',
		rankColor: 'sky',
		base: '3,500,000',
		meal: '200,000',
		traffic: '150,000',
		position: '-',
		allowance: '350,000',
		bank: '국민은행',
		account: '45****-67****',
		start: '2021.08.01',
		edit: true,
	},
	{
		id: 'EMP-004',
		name: '최지영',
		dept: '영업팀',
		rank: '사원',
		rankColor: 'green',
		base: '2,800,000',
		meal: '200,000',
		traffic: '100,000',
		position: '-',
		allowance: '300,000',
		bank: '하나은행',
		account: '11****-98****',
		start: '2023.01.09',
		edit: false,
	},
];

export default function SalaryBasic() {
	return (
		<main className="w-[1190px] bg-[#F3F6FA] p-[10px] text-[#1F2937]">
			{/* summary cards */}
			<div className="grid grid-cols-5 gap-3">
				<SummaryCard
					dark
					title="평균 기본급"
					value="3,662,500원"
					desc="전월 대비 +50,000원"
				/>
				<SummaryCard
					title="최고 기본급"
					value="4,700,000원"
					badge="이영희 · 차장"
				/>
				<SummaryCard
					blue
					title="월 총 인건비"
					value="29,300,000원"
					desc="기본급 합계 기준"
				/>
				<SummaryCard
					orange
					title="월 총 수당"
					value="3,340,000원"
					desc="수당 합계 기준"
				/>
				<SummaryCard green title="등록 인원" value="8명" desc="미등록 0명" />
			</div>

			{/* filter */}
			<section className="mt-4 flex h-[60px] items-center gap-4 rounded-[7px] border border-[#E5E7EB] bg-white px-5">
				<Filter label="부서" value="전체 부서" />
				<Filter label="직급" value="전체 직급" />

				<div className="flex items-center gap-2">
					<span className="text-[14px] font-bold">적용기준일</span>
					<div className="relative">
						<input
							value="2025.01.01"
							readOnly
							className="h-[34px] w-[110px] rounded-[5px] border border-[#D1D5DB] px-3 pr-8 text-[13px] font-bold text-[#6B7280]"
						/>
						<CalendarDays
							size={14}
							className="absolute right-3 top-1/2 -translate-y-1/2 text-[#9CA3AF]"
						/>
					</div>
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

				<button className="flex h-[34px] w-[82px] items-center justify-center gap-1 rounded-[5px] bg-[#183A6B] text-[13px] font-bold text-white">
					<Search size={14} />
					조회
				</button>

				<button className="flex h-[34px] w-[82px] items-center justify-center gap-1 rounded-[5px] border border-[#D1D5DB] bg-white text-[13px] font-bold text-[#6B7280]">
					<RotateCcw size={14} />
					초기화
				</button>
			</section>

			{/* table */}
			<section className="mt-4 overflow-hidden rounded-[7px] border border-[#E5E7EB] bg-white">
				<div className="flex h-[44px] items-center justify-between bg-[#F8FAFC] px-5">
					<div className="flex items-center gap-2 text-[15px] font-bold text-[#183A6B]">
						<Table2 size={16} />
						직원별 급여 기본정보
					</div>

					<div className="flex items-center gap-3 text-[12px]">
						<span className="rounded-full bg-[#DBEAFE] px-3 py-1 font-bold text-[#2563EB]">
							총 8명
						</span>
						<Legend color="bg-[#DBEAFE]" text="기본급" />
						<Legend color="bg-[#FEF9C3]" text="수당항목" />
						<Legend color="bg-[#DCFCE7]" text="계좌정보" />
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
							<Th w="90px">부서</Th>
							<Th w="70px">직급</Th>
							<Th color="blue" w="100px">
								기본급
							</Th>
							<Th color="yellow" w="75px">
								식대
							</Th>
							<Th color="yellow" w="75px">
								교통비
							</Th>
							<Th color="yellow" w="80px">
								직책수당
							</Th>
							<Th color="yellow" w="90px">
								수당합계
							</Th>
							<Th color="green" w="80px">
								은행
							</Th>
							<Th color="green" w="120px">
								계좌번호
							</Th>
							<Th w="95px">적용시작일</Th>
							<Th w="105px">관리</Th>
						</tr>
					</thead>

					<tbody>
						{rows.map((row) => (
							<tr
								key={row.id}
								className={`h-[43px] border-t ${
									row.edit ? 'bg-[#EFF6FF]' : 'bg-white'
								}`}
							>
								<td className="border border-[#E5E7EB]">
									<input type="checkbox" defaultChecked={row.edit} />
								</td>
								<Td>{row.id}</Td>
								<Td bold>{row.name}</Td>
								<Td>{row.dept}</Td>
								<Td>
									<RankBadge text={row.rank} color={row.rankColor} />
								</Td>
								<Td blue>
									{row.edit ? (
										<input
											value={row.base}
											readOnly
											className="h-[30px] w-[82px] rounded-[4px] border border-[#2563EB] bg-white text-center font-bold text-[#2563EB]"
										/>
									) : (
										row.base
									)}
								</Td>
								<Td yellow>{row.meal}</Td>
								<Td yellow>{row.traffic}</Td>
								<Td yellow>{row.position}</Td>
								<Td yellow strong>
									{row.allowance}
								</Td>
								<Td green>{row.bank}</Td>
								<Td green>{row.account}</Td>
								<Td>{row.start}</Td>
								<td className="border border-[#E5E7EB]">
									{row.edit ? (
										<div className="flex justify-center gap-1">
											<button className="flex items-center gap-1 rounded-[4px] bg-[#183A6B] px-2 py-1 text-[12px] font-bold text-white">
												<Save size={12} />
												저장
											</button>
											<button className="flex items-center gap-1 rounded-[4px] bg-[#FEF2F2] px-2 py-1 text-[12px] font-bold text-[#EF4444]">
												<X size={12} />
												취소
											</button>
										</div>
									) : (
										<div className="flex justify-center gap-1">
											<button className="flex items-center gap-1 rounded-[4px] bg-[#EFF6FF] px-2 py-1 text-[12px] font-bold text-[#2563EB]">
												<Pencil size={12} />
												수정
											</button>
											<button className="flex items-center gap-1 rounded-[4px] bg-[#F8FAFC] px-2 py-1 text-[12px] font-bold text-[#64748B]">
												<Clock size={12} />
												이력
											</button>
										</div>
									)}
								</td>
							</tr>
						))}
					</tbody>

					<tfoot>
						<tr className="h-[44px] bg-[#EAF2FF] font-bold text-[#183A6B]">
							<td
								colSpan={5}
								className="border border-[#BFDBFE] text-right pr-4"
							>
								Σ 합계 (8명)
							</td>
							<td className="border border-[#BFDBFE] text-[#2563EB]">
								29,300,000
							</td>
							<td className="border border-[#FEF3C7] text-[#B45309]">
								1,600,000
							</td>
							<td className="border border-[#FEF3C7] text-[#B45309]">
								1,000,000
							</td>
							<td className="border border-[#FEF3C7] text-[#B45309]">
								740,000
							</td>
							<td className="border border-[#FEF3C7] text-[#B45309] text-[16px]">
								3,340,000
							</td>
							<td className="border border-[#BFDBFE] text-[#94A3B8]">-</td>
							<td className="border border-[#BFDBFE] text-[#94A3B8]">-</td>
							<td className="border border-[#BFDBFE] text-[#94A3B8]">-</td>
							<td className="border border-[#BFDBFE] text-[#94A3B8]">-</td>
						</tr>
					</tfoot>
				</table>

				<div className="flex h-[44px] items-center justify-between px-5">
					<p className="text-[13px] text-[#64748B]">
						총 8명 조회 · 1명 수정 중
					</p>

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
		</main>
	);
}

function SummaryCard({ title, value, desc, badge, dark, blue, orange, green }) {
	let cls = 'bg-white border-[#E5E7EB] text-[#111827]';
	let valueCls = 'text-[#111827]';
	let titleCls = 'text-[#94A3B8]';

	if (dark) {
		cls = 'bg-[#183A6B] border-[#183A6B] text-white shadow-md';
		valueCls = 'text-white';
		titleCls = 'text-[#A9C4E8]';
	} else if (blue) {
		cls = 'bg-[#EFF6FF] border-[#BFDBFE]';
		valueCls = 'text-[#2563EB]';
		titleCls = 'text-[#2563EB]';
	} else if (orange) {
		cls = 'bg-[#FFFBEB] border-[#FACC15]';
		valueCls = 'text-[#B45309]';
		titleCls = 'text-[#D97706]';
	} else if (green) {
		cls = 'bg-[#F0FDF4] border-[#BBF7D0]';
		valueCls = 'text-[#16A34A]';
		titleCls = 'text-[#16A34A]';
	}

	return (
		<div
			className={`flex h-[74px] flex-col items-center justify-center rounded-[7px] border ${cls}`}
		>
			<p className={`text-[13px] font-bold ${titleCls}`}>{title}</p>
			<p className={`mt-1 text-[22px] font-extrabold ${valueCls}`}>{value}</p>
			{desc && (
				<p
					className={`text-[12px] font-bold ${dark ? 'text-[#7EA6D8]' : titleCls}`}
				>
					{desc}
				</p>
			)}
			{badge && (
				<span className="mt-1 rounded-full bg-[#E9D5FF] px-3 py-[2px] text-[12px] font-bold text-[#7C3AED]">
					{badge}
				</span>
			)}
		</div>
	);
}

function Filter({ label, value }) {
	return (
		<div className="flex items-center gap-2">
			<span className="text-[14px] font-bold">{label}</span>
			<button className="flex h-[34px] w-[140px] items-center justify-between rounded-[5px] border border-[#D1D5DB] px-3 text-[13px] text-[#6B7280]">
				{value}
				<ChevronDown size={14} className="text-[#9CA3AF]" />
			</button>
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

function Th({ children, color, w }) {
	const map = {
		blue: 'bg-[#EFF6FF] text-[#2563EB] border-[#BFDBFE]',
		yellow: 'bg-[#FFFBEB] text-[#D97706] border-[#FEF3C7]',
		green: 'bg-[#F0FDF4] text-[#16A34A] border-[#BBF7D0]',
	};

	return (
		<th
			style={{ width: w }}
			className={`border font-bold ${map[color] || 'border-[#E5E7EB]'}`}
		>
			{children}
		</th>
	);
}

function Td({ children, bold, blue, yellow, green, strong }) {
	return (
		<td
			className={`border border-[#E5E7EB] ${
				bold ? 'font-bold text-[#111827]' : 'text-[#4B5563]'
			} ${blue ? 'bg-[#EFF6FF] font-bold text-[#2563EB]' : ''} ${
				yellow ? 'bg-[#FFFBEB]' : ''
			} ${green ? 'bg-[#ECFDF5]' : ''} ${
				strong ? 'font-bold text-[#B45309]' : ''
			}`}
		>
			{children}
		</td>
	);
}

function RankBadge({ text, color }) {
	const map = {
		purple: 'bg-[#F3E8FF] text-[#8B5CF6]',
		blue: 'bg-[#DBEAFE] text-[#2563EB]',
		sky: 'bg-[#E0F2FE] text-[#0284C7]',
		green: 'bg-[#DCFCE7] text-[#16A34A]',
	};

	return (
		<span
			className={`rounded-full px-3 py-1 text-[12px] font-bold ${map[color]}`}
		>
			{text}
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
