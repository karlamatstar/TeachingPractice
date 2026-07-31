'use client';

import { useEffect, useState } from 'react';
import style from './Nav.module.css';
import { clsx } from 'clsx';
import { usePathname, useRouter } from 'next/navigation';

export default function Nav({
	initial = '',
	fullName = '',
	departmentName = '',
}) {
	const [activeNav, setActiveNav] = useState('');

	const router = useRouter();
	const pathname = usePathname();

	useEffect(() => {
		const lastPathaname = pathname.split('/').filter(Boolean).pop();

		switch (lastPathaname) {
			case 'register':
				setActiveNav('인사관리');
				break;
			default:
				setActiveNav('');
				break;
		}
	}, [pathname]);

	return (
		<div className={`${style.container}`}>
			<div className={style.left}>
				<div
					className={clsx(style.left1, 'cursor-pointer')}
					onClick={() => router.push('/info/register')}
				>
					<img src="/briefcase.png" />
					<span>인사관리시스템</span>
				</div>

				<div className={style.left2}>
					<ul className={clsx(style.navMenu, 'cursor-pointer')}>
						<li
							className={clsx(activeNav === '인사관리' ? style.active : '')}
							onClick={() => router.push('/info/register')}
						>
							인사관리
						</li>
						<li
							className={clsx(activeNav === '근태관리' ? style.active : '')}
							onClick={() => router.push('/work/attendance')}
						>
							근태관리
						</li>
						<li className={clsx(activeNav === '급여관리' ? style.active : '')}>
							급여관리
						</li>
						<li
							className={clsx(activeNav === '일용직관리' ? style.active : '')}
						>
							일용직관리
						</li>
					</ul>
				</div>
			</div>

			<div className={style.right}>
				{initial && fullName && (
					<>
						<img
							src="/Bell.png"
							className={`${style.imgIcon} ${style.bellIcon}`}
						/>
						<div className={style.nameWrapper}>
							<span className={style.circleInitial}>{initial}</span>
							<span className={style.fullName}>{fullName}</span>
						</div>
						<div className={style.departWrapper}>
							<span>{departmentName}</span>
							<img src="/logout.png" className={style.imgIcon} />
						</div>
					</>
				)}
			</div>
		</div>
	);
}
