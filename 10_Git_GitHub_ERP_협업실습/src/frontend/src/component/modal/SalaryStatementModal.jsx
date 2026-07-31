'use client';

import { Dialog, DialogContent, DialogTitle } from '@/components/ui/dialog';
import {
	ReceiptText,
	X,
	CalendarDays,
	TrendingUp,
	TrendingDown,
	CreditCard,
	Check,
	Mail,
	Printer,
	ShieldCheck,
} from 'lucide-react';

export default function SalaryStatementModal({ open, setOpen }) {
	return (
		<Dialog open={open} onOpenChange={setOpen}>
			<DialogContent className="w-[560px] max-w-[560px] p-0 overflow-hidden rounded-[14px] border-0">
				{/* Header */}
				<div className="flex h-[58px] items-center justify-between bg-[#1F4478] px-5 text-white">
					<div className="flex items-center gap-3">
						<ReceiptText size={22} className="text-[#93C5FD]" />
						<div>
							<DialogTitle className="text-[20px] font-bold">
								급여명세서
							</DialogTitle>
							<p className="text-[12px] text-[#93C5FD]">Salary Statement</p>
						</div>
					</div>

					<div className="flex items-center gap-2">
						<span className="rounded-full bg-[#3B6CA8] px-4 py-1 text-[13px] font-bold text-[#BFDBFE]">
							2025년 7월분
						</span>
						<button
							onClick={() => setOpen(false)}
							className="flex h-9 w-9 items-center justify-center rounded-[8px] bg-[#3569A5]"
						>
							<X size={20} />
						</button>
					</div>
				</div>

				{/* Company */}
				<div className="flex items-center justify-between border-b bg-[#F8FAFC] px-5 py-4">
					<div className="flex items-center gap-3">
						<div className="flex h-12 w-12 items-center justify-center rounded-[10px] bg-[#1F4478] text-[18px] font-bold text-white">
							HR
						</div>
						<div>
							<p className="text-[18px] font-bold text-[#111827]">
								주식회사 HRSystem
							</p>
							<p className="text-[13px] text-[#9CA3AF]">
								사업자등록번호: 123-45-67890 | 대표: 홍길동
							</p>
						</div>
					</div>

					<div className="text-right text-[13px] text-[#9CA3AF]">
						<p># PAY-2025-07-0008</p>
						<p className="mt-2 flex items-center gap-1">
							<CalendarDays size={14} /> 2025.08.01
						</p>
					</div>
				</div>

				<div className="bg-white px-5 py-4">
					<SectionTitle title="수급자 정보" />

					<div className="grid grid-cols-4 border-t border-l text-[14px]">
						<InfoLabel>성명</InfoLabel>
						<InfoValue>
							<span className="mr-2 inline-flex h-7 w-7 items-center justify-center rounded-full bg-[#DBEAFE] text-[12px] font-bold text-[#2563EB]">
								박
							</span>
							<b>박민준</b>
						</InfoValue>
						<InfoLabel>사원번호</InfoLabel>
						<InfoValue>EMP-003</InfoValue>

						<InfoLabel>부서</InfoLabel>
						<InfoValue>개발팀</InfoValue>
						<InfoLabel>직급</InfoLabel>
						<InfoValue>대리</InfoValue>

						<InfoLabel>지급연월</InfoLabel>
						<InfoValue>2025.07 (7.25 지급)</InfoValue>
						<InfoLabel>근속연수</InfoLabel>
						<InfoValue>3년 11개월</InfoValue>
					</div>
				</div>

				{/* Payment / Deduction */}
				<div className="grid grid-cols-2 border-y">
					<AmountBox
						title="지급항목"
						totalLabel="지급합계"
						total="4,200,000"
						color="blue"
						icon={<TrendingUp size={15} />}
						rows={[
							['기본급', '3,500,000'],
							['식대', '200,000'],
							['교통비', '150,000'],
							['야근수당', '350,000'],
							['직책수당', '-'],
						]}
					/>

					<AmountBox
						title="공제항목"
						totalLabel="공제합계"
						total="431,400"
						color="red"
						icon={<TrendingDown size={15} />}
						rows={[
							['국민연금 (4.5%)', '157,500'],
							['건강보험 (3.98%)', '139,300'],
							['고용보험 (0.9%)', '37,800'],
							['소득세', '88,000'],
							['지방소득세 (10%)', '8,800'],
						]}
					/>
				</div>

				{/* Real Payment */}
				<div className="bg-[#1F4478] px-5 py-5 text-white">
					<div className="flex items-center justify-between">
						<div>
							<p className="flex items-center gap-3 text-[18px] font-bold text-[#BFDBFE]">
								<span className="flex h-9 w-9 items-center justify-center rounded-[8px] bg-[#3569A5]">
									<CreditCard size={18} />
								</span>
								실 지급액
							</p>
							<p className="mt-2 text-[13px] text-[#93C5FD]">
								4,200,000 - 431,400
							</p>
						</div>

						<div className="text-right">
							<p className="text-[34px] font-extrabold">3,768,600</p>
							<p className="text-[13px] text-[#BFDBFE]">원 (KRW)</p>
						</div>
					</div>

					<div className="mt-4 rounded-[7px] bg-[#3569A5] py-2 text-center text-[13px] text-[#BFDBFE]">
						㉿ 삼백칠십육만팔천육백원정 (₩3,768,600)
					</div>

					<div className="mt-4 flex items-center justify-center gap-3 text-[13px] font-bold">
						<span className="rounded-full bg-[#3569A5] px-4 py-2 text-[#93C5FD]">
							↑ 지급 4,200,000원
						</span>
						<span className="text-[#93C5FD]">−</span>
						<span className="rounded-full bg-[#3569A5] px-4 py-2 text-[#FCA5A5]">
							↓ 공제 431,400원
						</span>
						<span className="text-[#93C5FD]">=</span>
						<span className="rounded-full bg-white px-4 py-2 text-[#1F4478]">
							✓ 실지급 3,768,600원
						</span>
					</div>
				</div>

				{/* Summary */}
				<div className="flex h-[42px] items-center justify-between border-b bg-[#EFF6FF] px-5 text-[13px] font-bold">
					<div className="flex items-center gap-2 text-[#2563EB]">
						<CalendarDays size={15} />
						7월 근태 요약
					</div>
					<div className="flex gap-3 text-[#4B5563]">
						<span className="text-[#2563EB]">● 출근 20일</span>
						<span>|</span>
						<span className="text-[#16A34A]">● 연차 1일</span>
						<span>|</span>
						<span className="text-[#8B5CF6]">● 야근 7시간</span>
						<span>|</span>
						<span className="text-[#EA580C]">● 지각 0회</span>
					</div>
				</div>

				{/* Confirm */}
				<div className="relative bg-white px-5 py-4">
					<SectionTitle title="확인 및 직인" />

					<p className="mt-5 text-[14px] leading-7 text-[#4B5563]">
						위 금액을 급여로 지급함을 확인합니다.
						<br />
						<b>지급일: 2025년 7월 25일</b>
						<br />
						<b>주식회사 HRSystem 대표이사 홍 길 동 (인)</b>
					</p>

					<div className="absolute bottom-8 right-8 flex h-[88px] w-[88px] items-center justify-center rounded-full border-[3px] border-[#1F4478] text-[26px] font-bold text-[#1F4478]">
						직<br />인
					</div>

					<div className="mt-5 rounded-[6px] border border-[#FACC15] bg-[#FFFBEB] px-4 py-3 text-[13px] font-bold text-[#B45309]">
						ⓘ 본 명세서는 전자문서로 발행되었으며 위변조 시 법적 처벌을 받을 수
						있습니다.
					</div>
				</div>

				{/* Footer */}
				<div className="flex h-[58px] items-center justify-between border-t bg-[#F8FAFC] px-5">
					<div className="flex items-center gap-4 text-[13px]">
						<span className="flex items-center gap-1 rounded-full bg-[#EFF6FF] px-4 py-2 font-bold text-[#2563EB]">
							<ShieldCheck size={15} />
							전자문서 인증완료
						</span>
						<span className="text-[#9CA3AF]">CERT-2025-0089</span>
					</div>

					<div className="flex gap-2">
						<button className="flex h-[38px] items-center gap-2 rounded-[6px] border px-4 text-[14px] font-bold text-[#4B5563]">
							<Mail size={16} />
							이메일 발송
						</button>
						<button className="flex h-[38px] items-center gap-2 rounded-[6px] bg-[#1F4478] px-5 text-[14px] font-bold text-white">
							<Printer size={16} />
							인쇄
						</button>
						<button
							onClick={() => setOpen(false)}
							className="flex h-[38px] items-center gap-2 rounded-[6px] border px-4 text-[14px] font-bold text-[#4B5563]"
						>
							<X size={16} />
							닫기
						</button>
					</div>
				</div>
			</DialogContent>
		</Dialog>
	);
}

function SectionTitle({ title }) {
	return (
		<h3 className="flex items-center gap-2 border-l-4 border-[#1F4478] pl-2 text-[16px] font-bold text-[#1F4478]">
			{title}
		</h3>
	);
}

function InfoLabel({ children }) {
	return (
		<div className="border-r border-b bg-[#F8FAFC] px-4 py-3 font-bold text-[#6B7280]">
			{children}
		</div>
	);
}

function InfoValue({ children }) {
	return (
		<div className="border-r border-b px-4 py-3 font-bold text-[#374151]">
			{children}
		</div>
	);
}

function AmountBox({ title, rows, totalLabel, total, color, icon }) {
	const isBlue = color === 'blue';

	return (
		<div className={isBlue ? 'border-r' : ''}>
			<div
				className={`flex h-[42px] items-center justify-between px-5 font-bold ${
					isBlue ? 'bg-[#EFF6FF] text-[#2563EB]' : 'bg-[#FEF2F2] text-[#DC2626]'
				}`}
			>
				<span className="flex items-center gap-1">
					{icon}
					{title}
				</span>
				<span className="text-[13px] opacity-60">금액 (원)</span>
			</div>

			{rows.map(([label, value]) => (
				<div
					key={label}
					className={`flex h-[40px] items-center justify-between border-t px-5 text-[15px] ${
						isBlue ? 'bg-white' : 'bg-[#FFFBFB]'
					}`}
				>
					<span className="font-bold text-[#4B5563]">
						<b className={isBlue ? 'text-[#BFDBFE]' : 'text-[#FECACA]'}>●</b>{' '}
						{label}
					</span>
					<span
						className={`font-extrabold ${
							isBlue ? 'text-[#2563EB]' : 'text-[#EF4444]'
						}`}
					>
						{value}
					</span>
				</div>
			))}

			<div
				className={`flex h-[48px] items-center justify-between border-t px-5 text-[18px] font-extrabold ${
					isBlue ? 'bg-[#EFF6FF] text-[#1D4ED8]' : 'bg-[#FEF2F2] text-[#991B1B]'
				}`}
			>
				<span>{totalLabel}</span>
				<span>{total}</span>
			</div>
		</div>
	);
}
