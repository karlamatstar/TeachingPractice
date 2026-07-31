'use client';

import c from './ViewTable.module.css';
import { clsx } from 'clsx';

const dummy = [
	{
		no: 1,
		employeeNumber: 'EMP-001',
		name: '김철수',
		department: '인사팀',
		position: '팀장',
		hireDate: '2019.03.02',
		phone: '010-2020-3030',
		email: 'kim@company.com',
		status: '재직중',
	},
	{
		no: 2,
		employeeNumber: 'EMP-002',
		name: '이영희',
		department: '개발팀',
		position: '대리',
		hireDate: '2020.07.15',
		phone: '010-1111-2222',
		email: 'lee@company.com',
		status: '재직중',
	},
	{
		no: 3,
		employeeNumber: 'EMP-003',
		name: '박민수',
		department: '영업팀',
		position: '과장',
		hireDate: '2018.11.20',
		phone: '010-3333-4444',
		email: 'park@company.com',
		status: '휴직중',
	},
	{
		no: 4,
		employeeNumber: 'EMP-004',
		name: '최지은',
		department: '마케팅팀',
		position: '사원',
		hireDate: '2022.01.10',
		phone: '010-5555-6666',
		email: 'choi@company.com',
		status: '재직중',
	},
	{
		no: 5,
		employeeNumber: 'EMP-005',
		name: '정우성',
		department: '총무팀',
		position: '부장',
		hireDate: '2015.05.18',
		phone: '010-7777-8888',
		email: 'jung@company.com',
		status: '퇴사',
	},
	{
		no: 6,
		employeeNumber: 'EMP-006',
		name: '한지민',
		department: '디자인팀',
		position: '대리',
		hireDate: '2021.09.03',
		phone: '010-9999-0000',
		email: 'han@company.com',
		status: '재직중',
	},
	{
		no: 7,
		employeeNumber: 'EMP-007',
		name: '오세훈',
		department: '기획팀',
		position: '차장',
		hireDate: '2017.12.01',
		phone: '010-1212-3434',
		email: 'oh@company.com',
		status: '재직중',
	},
	{
		no: 8,
		employeeNumber: 'EMP-008',
		name: '유나영',
		department: '재무팀',
		position: '과장',
		hireDate: '2019.08.25',
		phone: '010-5656-7878',
		email: 'yu@company.com',
		status: '휴직중',
	},
	{
		no: 9,
		employeeNumber: 'EMP-009',
		name: '강동원',
		department: '물류팀',
		position: '사원',
		hireDate: '2023.04.11',
		phone: '010-9090-1010',
		email: 'kang@company.com',
		status: '재직중',
	},
	{
		no: 10,
		employeeNumber: 'EMP-010',
		name: '송혜교',
		department: 'CS팀',
		position: '팀장',
		hireDate: '2016.06.30',
		phone: '010-2323-4545',
		email: 'song@company.com',
		status: '퇴사',
	},
];
const dummyColumns = [
	'NO',
	'사원번호',
	'성명',
	'부서',
	'직급',
	'입사일',
	'연락처',
	'이메일',
	'재직상태',
	'관리',
];

export default function ViewTable({
	renderRow,
	columns = dummyColumns,
	rowList = dummy,
	renderTitle,
	isShowTopTotalCount = false,
	smallColumnIdxList = [],
	selectedRowIdx,
	setSelectedRowIdx,
}) {
	return (
		<div className={c.container} id="viewtable">
			{(typeof renderTitle === 'function' || isShowTopTotalCount) && (
				<div className={c.topInfo}>
					<div className={c.titleArea}>{renderTitle()}</div>

					<div>
						<span className={c.totalCountText}>총 {rowList.length}건</span>
					</div>
				</div>
			)}

			<ul className={c.columnRow}>
				{columns.map((item, idx) => (
					<li
						key={idx}
						className={clsx(
							smallColumnIdxList.includes(idx) ? 'flex-[0.5]' : 'flex-1'
						)}
					>
						{item}
					</li>
				))}
			</ul>

			{rowList.map((item, idx) => (
				<ul
					key={idx}
					className={clsx(
						c.itemRow,
						Number.isFinite(selectedRowIdx) &&
							selectedRowIdx === idx &&
							c.itemSelectedActive,
						'cursor-pointer'
					)}
					onClick={() => {
						if (Number.isFinite(selectedRowIdx)) {
							setSelectedRowIdx(idx);
						}
					}}
				>
					{renderRow(item, idx)}
				</ul>
			))}

			{/*총갯수 및 페이징*/}
			<div className={c.totalCountContainer}>
				<span className={c.totalCount}>총 {rowList.length}건</span>

				<div className={c.pagingWrapper}>
					{/*<span>*/}
					{/*  <ChevronLeft/>*/}
					{/*</span>*/}

					<ul className={c.numbering}>
						<li className={c.active}>1</li>
						{/*<li>2</li>*/}
						{/*<li>3</li>*/}
					</ul>

					{/*<span>*/}
					{/*  <ChevronRight/>*/}
					{/*</span>*/}
				</div>
			</div>
		</div>
	);
}
