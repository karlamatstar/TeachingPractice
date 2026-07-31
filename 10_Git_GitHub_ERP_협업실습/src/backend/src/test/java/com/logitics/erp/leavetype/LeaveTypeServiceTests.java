package com.logitics.erp.leavetype;

import com.logitics.erp.leavetype.entity.LeaveType;
import com.logitics.erp.leavetype.repository.LeaveTypeRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
public class LeaveTypeServiceTests {

	@Autowired
	private LeaveTypeRepository leaveTypeRepository;

	@Test
	@DisplayName("특별휴가정책 추가")
	public void createLeaveType() {
		List<LeaveType> list = List.of(
						new LeaveType("결혼휴가", false, 5.0, ""),
						new LeaveType("출산휴가(여)", false, 90.0, ""),
						new LeaveType("배우자 출산 휴가", false, 10.0, ""),
						new LeaveType("부모사망", false, 5.0, ""),
						new LeaveType("배우자/자녀사망", false, 3.0, ""),
						new LeaveType("형제사망", false, 1.0, "")
		);

		leaveTypeRepository.saveAll(list);
	}

}
