package com.logitics.erp.employeeeventsupport.service;

import com.logitics.erp.employeeeventsupport.dto.EmployeeEventSupportRegisterRequest;
import com.logitics.erp.employeeeventsupport.dto.EmployeeEventSupportResponse;
import com.logitics.erp.employeeeventsupport.entity.EmployeeEventSupport;
import com.logitics.erp.employeeeventsupport.mapper.EmployeeEventSupportMapper;
import com.logitics.erp.employeeeventsupport.repository.EmployeeEventSupportRepository;
import jakarta.transaction.Transactional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class EmployeeEventSupportService {

	private final EmployeeEventSupportMapper employeeEventSupportMapper;
	private final EmployeeEventSupportRepository employeeEventSupportRepository;

	public List<EmployeeEventSupportResponse> getSupportList(int page, int size, String keyword, Long employeeId) {
		int offset = page * size;
		return employeeEventSupportMapper.getSupportList(size, offset, keyword, employeeId);
	}

    @Transactional
	public boolean registerEventSupport(EmployeeEventSupportRegisterRequest registerRequest) {

        try {
            // 1. 경조사비 폼 데이터 먼저 등록
            employeeEventSupportMapper.registerEventSupport(registerRequest);
//            Long registeredId = registerRequest.getEmployeeEventSupportId();
            Long registeredId = employeeEventSupportRepository.findAll().getLast().getEmployeeEventSupportId();

            // 2. 업로드한 파일이 존재하는 경우) fileAttachment > ref_id 업데이트 시킨다.
            List<Long> list = registerRequest.getFileIdList();
            if (list != null && !list.isEmpty()) {
                Long fileId = list.getLast();
                employeeEventSupportMapper.updateFileRefId(fileId, registeredId) ;
            }

            return true;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
	}

	public boolean deleteEventSupport(Long eventSupportId) {
		return employeeEventSupportMapper.deleteEventSupport(eventSupportId) > 0;
	}

    public EmployeeEventSupportResponse getEventSupportDetail(Long eventSupportId) {
        return employeeEventSupportMapper.getEventSupportDetail(eventSupportId);
    }
}
