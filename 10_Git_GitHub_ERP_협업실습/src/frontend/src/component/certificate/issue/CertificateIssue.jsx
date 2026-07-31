'use client';

import {
	BriefcaseBusiness,
	Medal,
	Banknote,
	ReceiptText,
	ClipboardCheck,
	FileText,
	Lock,
	ChevronDown,
	Minus,
	Plus,
	Languages,
	Calendar,
	Eye,
	X,
	Printer,
} from 'lucide-react';

const certificates = [
	{
		title: '재직증명서',
		desc: '현재 재직 중임을 증명합니다',
		icon: BriefcaseBusiness,
		selected: true,
	},
	{
		title: '경력증명서',
		desc: '경력 사항을 증명합니다',
		icon: Medal,
	},
	{
		title: '급여확인서',
		desc: '급여 내역을 확인합니다',
		icon: Banknote,
	},
	{
		title: '근로소득원천징수',
		desc: '원천징수 내역 확인서',
		icon: ReceiptText,
	},
];

export default function CertificateIssuePage() {
	return (
		<main className="w-[1190px] bg-[#F3F6FA] p-[10px] text-[#1F2937]">
			{/* 증명서 종류 선택 */}
			<section className="overflow-hidden rounded-[8px] border border-[#E5E7EB] bg-white">
				<SectionHeader
					icon={<ClipboardCheck size={16} />}
					title="증명서 종류 선택"
					requiredText="필수 선택"
				/>

				<div className="grid grid-cols-4 gap-3 border-t border-[#E5E7EB] p-5">
					{certificates.map((item) => (
						<CertificateCard key={item.title} {...item} />
					))}
				</div>
			</section>

			{/* 발급 정보 입력 */}
			<section className="mt-4 overflow-hidden rounded-[8px] border border-[#E5E7EB] bg-white">
				<SectionHeader
					icon={<FileText size={16} />}
					title="발급 정보 입력"
					badge="재직증명서 발급 중"
				/>

				<div className="border-t border-[#E5E7EB] p-5">
					<SubTitle title="신청자 정보" />

					<div className="grid grid-cols-[150px_130px_150px_120px_150px] gap-3">
						<ReadOnlyInput label="사원번호" value="EMP-002" />
						<ReadOnlyInput label="성명" value="이영희" />
						<ReadOnlyInput label="부서" value="경영지원팀" />
						<ReadOnlyInput label="직급" value="과장" />
						<ReadOnlyInput label="입사일" value="2018.07.15" />
					</div>

					<div className="my-5 h-px bg-[#E5E7EB]" />

					<SubTitle title="발급 상세 정보" />

					<div className="grid grid-cols-[200px_240px_120px_170px] gap-3">
						<Field label="용도" required>
							<button className="flex h-[36px] w-full items-center justify-between rounded-[5px] border border-[#D1D5DB] px-3 text-[13px]">
								관광서 제출용
								<ChevronDown size={14} className="text-[#9CA3AF]" />
							</button>
						</Field>

						<Field label="제출처" required>
							<input
								className="h-[36px] w-full rounded-[5px] border border-[#D1D5DB] px-3 text-[13px] outline-none"
								placeholder="예: 국민은행 ○○지점"
							/>
						</Field>

						<Field label="발급부수" required>
							<div className="flex h-[36px] items-center">
								<button className="flex h-full w-[36px] items-center justify-center rounded-l-[5px] bg-[#F9FAFB]">
									<Minus size={14} />
								</button>
								<div className="flex h-full w-[48px] items-center justify-center border-x border-[#E5E7EB] text-[14px] font-bold">
									1
								</div>
								<button className="flex h-full w-[36px] items-center justify-center rounded-r-[5px] bg-[#F9FAFB]">
									<Plus size={14} />
								</button>
							</div>
						</Field>

						<Field label="언어선택" required>
							<div className="grid h-[36px] grid-cols-2 overflow-hidden rounded-[5px] border border-[#D1D5DB]">
								<button className="flex items-center justify-center gap-1 bg-[#183A6B] text-[13px] font-bold text-white">
									<Languages size={14} />
									국문
								</button>
								<button className="flex items-center justify-center gap-1 bg-white text-[13px] text-[#6B7280]">
									<Languages size={14} />
									영문
								</button>
							</div>
						</Field>
					</div>

					<div className="mt-3 grid grid-cols-[180px_1fr] gap-3">
						<Field label="기준일">
							<div className="relative">
								<input
									className="h-[36px] w-full rounded-[5px] border border-[#D1D5DB] px-3 pr-9 text-[13px]"
									value="2025.07.01"
									readOnly
								/>
								<Calendar
									size={15}
									className="absolute right-3 top-1/2 -translate-y-1/2 text-[#9CA3AF]"
								/>
							</div>
						</Field>

						<Field label="발급목적 (선택)">
							<input
								className="h-[36px] w-full rounded-[5px] border border-[#D1D5DB] px-3 text-[13px] outline-none"
								placeholder="발급 목적을 간략히 입력하세요"
							/>
						</Field>
					</div>

					<div className="my-5 h-px bg-[#E5E7EB]" />

					<div className="flex items-center justify-between rounded-[7px] border border-[#FACC15] bg-[#FFFBEB] px-4 py-3">
						<div className="flex items-start gap-3">
							<Eye size={16} className="mt-[3px] text-[#D97706]" />
							<div>
								<p className="text-[14px] font-bold text-[#92400E]">
									출력 전 미리보기를 확인하세요
								</p>
								<p className="mt-1 text-[12px] text-[#D97706]">
									발급된 증명서는 위변조 방지 마크가 포함됩니다. 내용을 반드시
									확인한 후 출력해 주세요.
								</p>
							</div>
						</div>

						<button className="flex h-[34px] items-center gap-1 rounded-[5px] border border-[#FBBF24] bg-white px-4 text-[13px] font-bold text-[#D97706]">
							<Eye size={14} />
							미리보기
						</button>
					</div>

					<div className="mt-4 flex justify-end gap-2">
						<button className="flex h-[38px] w-[90px] items-center justify-center gap-1 rounded-[5px] border border-[#D1D5DB] bg-white text-[14px] font-bold text-[#4B5563]">
							<X size={15} />
							취소
						</button>

						<button className="flex h-[38px] w-[108px] items-center justify-center gap-1 rounded-[5px] border border-[#CBD5E1] bg-[#F1F5F9] text-[14px] font-bold text-[#334155]">
							<Eye size={15} />
							미리보기
						</button>

						<button className="flex h-[38px] w-[108px] items-center justify-center gap-1 rounded-[5px] bg-[#183A6B] text-[14px] font-bold text-white">
							<Printer size={15} />
							출력하기
						</button>
					</div>
				</div>
			</section>
		</main>
	);
}

function SectionHeader({ icon, title, requiredText, badge }) {
	return (
		<div className="flex h-[44px] items-center justify-between px-5">
			<div className="flex items-center gap-2">
				<span className="text-[#183A6B]">{icon}</span>
				<h2 className="text-[15px] font-bold text-[#183A6B]">{title}</h2>
				{requiredText && (
					<span className="ml-2 text-[12px] text-[#9CA3AF]">
						<b className="mr-1 text-red-500">*</b> {requiredText}
					</span>
				)}
			</div>

			{badge && (
				<span className="rounded-full bg-[#DBEAFE] px-4 py-1 text-[13px] font-bold text-[#2563EB]">
					{badge}
				</span>
			)}
		</div>
	);
}

function CertificateCard({ title, desc, icon: Icon, selected }) {
	return (
		<button
			className={`flex h-[170px] flex-col items-center justify-center rounded-[8px] border transition ${
				selected
					? 'border-[2px] border-[#2563EB] bg-[#EFF6FF]'
					: 'border-[#E5E7EB] bg-white'
			}`}
		>
			<div
				className={`flex h-[48px] w-[48px] items-center justify-center rounded-[13px] ${
					selected
						? 'bg-[#DBEAFE] text-[#2563EB]'
						: 'bg-[#F1F5F9] text-[#6B7280]'
				}`}
			>
				<Icon size={24} />
			</div>

			<p className="mt-4 text-[16px] font-bold">{title}</p>
			<p className="mt-2 text-[12px] text-[#9CA3AF]">{desc}</p>

			<span
				className={`mt-4 rounded-full px-4 py-1 text-[12px] font-bold ${
					selected ? 'bg-[#2563EB] text-white' : 'bg-[#F1F5F9] text-[#9CA3AF]'
				}`}
			>
				{selected ? '✓ 선택됨' : '선택하기'}
			</span>
		</button>
	);
}

function SubTitle({ title }) {
	return (
		<h3 className="mb-3 border-l-[4px] border-[#183A6B] pl-2 text-[14px] font-bold text-[#183A6B]">
			{title}
		</h3>
	);
}

function ReadOnlyInput({ label, value }) {
	return (
		<div>
			<label className="mb-1 block text-[13px] font-bold">{label}</label>
			<div className="relative">
				<input
					value={value}
					readOnly
					className="h-[36px] w-full rounded-[5px] border border-[#D1D5DB] bg-[#F9FAFB] px-3 pr-8 text-[13px] font-bold text-[#4B5563]"
				/>
				<Lock
					size={14}
					className="absolute right-3 top-1/2 -translate-y-1/2 text-[#9CA3AF]"
				/>
			</div>
		</div>
	);
}

function Field({ label, required, children }) {
	return (
		<div>
			<label className="mb-1 block text-[13px] font-bold">
				{label} {required && <span className="text-red-500">*</span>}
			</label>
			{children}
		</div>
	);
}
