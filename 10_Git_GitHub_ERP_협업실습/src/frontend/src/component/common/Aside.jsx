'use client';

import s from './Aside.module.css'
import {usePathname, useRouter} from "next/navigation";
import {clsx} from "clsx";

export default function Aside({menus}) {
	
	const router = useRouter();
	const pathname = usePathname()
	const lastPathname = pathname.split("/").filter(Boolean).pop();
	
	return (
		<div className={s.container}>
			{menus.map((item, index) => (
				<div className={s.menuItem} key={index}>
					<p className={s.menuTitle}>
						<img className={s.img13} src={item.titleInfo.iconPath} alt=""/>
						{item.titleInfo.title}
					</p>
					
					<ul className={s.menuSub}>
						{item.subMenus.map((subItem, subIdx) => (
							<li
								key={subIdx}
								className={
									clsx(pathname === subItem.path ? s.active : undefined, "cursor-pointer")
								}
								onClick={() => router.push(subItem.path || "/")}
							>
								{subItem.title}
							</li>
						))}
					</ul>
				
				</div>
			))}
		</div>
	)
}